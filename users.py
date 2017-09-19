from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json

db_connect = create_engine('sqlite:///test_data.db')
app = Flask(__name__)
api = Api(app)

#class to display all the books in wishlist
class books(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from main.book")
        return {'books': [i[0] for i in query.cursor.fetchall()]} 

#class to add books in wishlist
class add(Resource):
    def post(self):
        conn = db_connect.connect()
        data_dict = (eval(request.data))
        print data_dict['author']

        title = data_dict['title']
        author = data_dict['author']
        isbn = data_dict['isbn']
        date_of_publication = data_dict['date_of_publication']

        query = conn.execute("insert into book (title,author,isbn,date_of_publication) values(?,?,?,?)",(title,author,isbn,date_of_publication))
        return {'status':'success'}        

#class to delete books from wishlist
class remove(Resource):
    def delete(self):
        conn = db_connect.connect()
        data_dict = (eval(request.data))
        isbn = data_dict['isbn']
        
        query = conn.execute("DELETE FROM book WHERE isbn =" + str(isbn))
        return {'status':'success'}

#class to update books from wishlist
class update(Resource):
    def put(self):
        conn = db_connect.connect()
        data_dict = (eval(request.data))
        isbn = data_dict['isbn']
        title = data_dict['title']
        author = data_dict['author']
        date_of_publication = data_dict['date_of_publication']
        print isbn, title, author, date_of_publication

        query = conn.execute('''UPDATE book set title = ?, author = ?, date_of_publication = ? WHERE isbn = ? ''' ,(title,author,date_of_publication,isbn))
        return {'status':'success'}


api.add_resource(books, '/')
api.add_resource(add, '/add', methods=['POST'])
api.add_resource(remove, '/delete',methods=['DELETE'])
api.add_resource(update, '/update', methods=['PUT'])

if __name__ == '__main__':
     app.run(port='5010')