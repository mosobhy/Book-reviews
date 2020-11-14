import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helper import login_required
import requests

# configure the flask app
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/user_reveiw/<int:book_id>', methods=['POST'])
@login_required
def user_reveiw(book_id):
    """ This function is going to insert the users' reviews into db """
    # access the form fileds
    user_rate = request.form.get('user_rate')
    text_reveiw = request.form.get('text_reveiw')

    if not user_rate or not text_reveiw:
        return render_template('error.html', message='You have to rate our book pls')

    # insert these data into db
    db.execute('''
        INSERT INTO reviews(
            user_id,
            book_id,
            user_rate,
            review
        )
        VALUES(
            :var1,
            :var2,
            :var3,
            :var4
        )
    ''', {
        'var1': session['id'],
        'var2': book_id,
        'var3': int(user_rate),
        'var4': text_reveiw
    })
    db.commit()

    return redirect('/')


@app.route('/reveiws/<string:book_isbn>', methods=['GET', 'POST'])
@login_required
def reveiw(book_isbn):
    """ Render the review tempalte and talk to the API """

    if request.method == 'GET':     # i used GET, cuz, the index.html redirect to it with get
        # retrieve the selected book data from db
        book_data = db.execute('SELECT * FROM books WHERE isbn=:var1', {'var1': book_isbn}).fetchone()
        if not book_data:
            return render_template('error.html', message='Something went wrong!')

        print(book_data.title)
        print(book_data.isbn)
        # set my api key.
        api_key = "YABOjuXGoBgLI1C2IjdA"

        # contact the API to get its reveiws.
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": book_isbn})
        if res.status_code != 200:
            return render_template('error.html', message='API failed, try later!')

        # now exctract the respons and convert into json
        work_ratings_count = res.json()['books'][0]['work_ratings_count']
        ave_rating = res.json()['books'][0]['average_rating']

        # contact the book covers api.
        book_cover = f'http://covers.openlibrary.org/b/ISBN/{book_isbn}-L.jpg'

        # pass reviews to the template ( as variables )
        return render_template('reveiw.html',
                            book_data=book_data,
                            work_ratings_count=work_ratings_count,
                            ave_rating=ave_rating,
                            book_cover=book_cover
                        )

    else:
        return render_template('reveiw.html')

@app.route("/", methods=['GET', 'POST'])
@login_required     # to be implemented
def index():
    """ searchs for a book or books using isbn, title, author """

    if request.method == 'POST':
        # access the form data
        book_data = request.form.get('book')

        if not book_data:
            return render_template('error.html', message='What Book?')

        # retrieve the whole matching books from the db
        resulted_books = db.execute(f"""
            SELECT * FROM books
            WHERE
                isbn LIKE('%{book_data}%')
            OR
                title LIKE('%{book_data}%')
            OR
                author LIKE('%{book_data}%')
        """).fetchall()

        if not resulted_books:
            return render_template('error.html', message='No matches!')

        return render_template('index.html', resulted_books=resulted_books)
    
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ register a user into db """

    if request.method == 'POST':
        name = request.form.get('name')
        handle = request.form.get('handle')
        password = request.form.get('password')

        if not name or not handle or not password:
            return render_template('error.html', message='Complete all form entries')
        
        # check that the handle is not in db.
        if db.execute('SELECT handle FROM users WHERE handle = :var1', {'var1': handle}).fetchone():
            return render_template('error.html', message='Handle already exist')        

        # load the new user into the db
        db.execute("""
            INSERT INTO users(
                name,
                handle,
                password
            )
            VALUES(
                :var1,
                :var2,
                :var3
            )
        """, {
            'var1': name,
            'var2': handle,
            'var3': password
        })
        db.commit()

        # now rediect him to index
        return redirect('/')

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ log a user into the app using session dict """

    # clear the session before loging in
    session.clear()

    if request.method == 'POST':
        # access the login data from login.html
        handle = request.form.get('handle')
        password = request.form.get('password')

        if not handle or not password:
            return render_template('error.html', message='Please, complete all form entries')

        # validate the data 
        user_data  = db.execute("""
            SELECT * FROM users
            WHERE
                handle = :var1
            AND 
                password = :var2
        """, {
            'var1': handle,
            'var2': password
        }).fetchone()
        
        # if user exist, log him in
        if user_data:
            session['id'] = user_data.id
            session['handle'] = user_data.handle
        else:
            return render_template('error.html', message='Invalid data')

        return redirect('/')

    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():

    session.clear()

    return redirect('/login')


@app.route('/api/<string:isbn>', methods=['GET'])
def api(isbn):
    """ Return a json object of book data """
    from flask import jsonify

    # validate upon the input
    try:
        requested_book = db.execute("""
            SELECT * FROM books
            WHERE
                isbn = :var1
        """, {
            'var1': isbn
        }).fetchone()

        return jsonify({
            "title": requested_book.title,
            "author": requested_book.author,
            "year": requested_book.pulication_year,
            "isbn": requested_book.isbn,
        }), 200

    except:
        return jsonify({'error': 'Invalid ISBN', 'status code': 404}), 404