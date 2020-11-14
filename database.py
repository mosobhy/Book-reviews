from flask import Flask
from models import *

# configure the flask app
app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///mydb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create a shared object of db
db.init_app(app)

def main():
    # create the database tables.
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        main()