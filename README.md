# Project 1

Web Programming with Python and JavaScript

1. designed the database schema
    models.py ==> defined the table classes
    database.py ==> executed the models.py
    
2. loaded the books into database
    import.py ==> loaded the books.csv into the books table

3. designed the layout.html tempalte
4. designed the login, regiser, index(results), reviews templates

5. desigen the review tempalte
6. reveiw route and how you are gonna talk to the book_api and cover_api.


7. all the enhancements that's required is to protect against the sql injections in index route
    it requires to be redesigned in such a way that detect the input pattern and use the convenient sql constraint.. using regex or whatever

8. designed the API at (/api/$isbn)