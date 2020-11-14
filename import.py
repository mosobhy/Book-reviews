"""
In this script, we are going to load all the books from books.csv and insert it
into the database in books tables
"""
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# configure the database to connect
engine = create_engine('postgresql:///mydb')
db = scoped_session(sessionmaker(bind=engine))

# open the csv file containing the books
with open('books.csv') as file:

    # create a reader object
    reader = csv.reader(file)

    # iterate over file
    for isbn, title, author, year in reader:
        try:
            db.execute('''
                INSERT INTO books(
                    isbn,
                    title, 
                    author, 
                    pulication_year
                )
                VALUES(
                    :var1,
                    :var2,
                    :var3,
                    :var4
                )
                ''', {
                    'var1': isbn,
                    'var2': title,
                    'var3': author,
                    'var4': year
                })
            db.commit()

        except Exception as e:
            raise e