from flask_sqlalchemy import SQLAlchemy

# instatiate a database object
db = SQLAlchemy()

# create the table classes
class User(db.Model):
    """ This will represents the users table """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    handle = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Book(db.Model):
    """ This will represents the books table """

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    pulication_year = db.Column(db.String, nullable=False)


class Review(db.Model):
    """ This will represents the reviews table """

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_rate = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
