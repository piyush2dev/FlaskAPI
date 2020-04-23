import datetime
from json import dumps
import jwt
from flask import Flask, request, Response
from BookModel import *

app.config['SECRET_KEY'] = 'meow'

# login method
@app.route("/login")
def login():
    expiry_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    # jwt will return a token on basis of info provided
    token = jwt.encode({'exp':expiry_date},app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route("/")
def hello_world():
    return 'Hello World!'


@app.route("/<name>")
def hello_name(name):
    return "Hello" + name


# GET all books
# /books?token=jaluwnc;owndvou;njcKHDGIWF;SJBC;ASJVDSOJ
@app.route("/books")
def get_books():
    token = request.args.get('token')
    try:
        jwt.decode(token,app.config['SECRET_KEY'])
    except:
        return jsonify({'error': "need a valid token"})
    return jsonify({'book': get_all_book()})


# GET book by isbn
@app.route("/books/<isbn>")
def get_book_by_isbn(isbn):
    value = get_Book(isbn)
    return jsonify(value)


# valid data check method
def validBookObject(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        False


# POST BOOK
@app.route("/books", methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        # new_book = {
        #     "name": request_data['name'],
        #     "price": request_data['price'],
        #     "isbn": request_data['isbn']
        # }
        add_Book(request_data['name'],request_data['price'],request_data['isbn'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalid_error_msg = {"error": "Invalid request",
                             "msg": "pass data like name ,price,isbn"}
        response = Response(json.dumps(invalid_error_msg), status=400, mimetype='application/json')
        return response


# replace book by isbn
@app.route("/books/<int:isbn>", methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if (not validBookObject(request_data)):
        invalid_error_msg = {"error": "Invalid request",
                             "msg": "pass data like name ,price,isbn"}
        response = Response(json.dumps(invalid_error_msg), status=400, mimetype='application/json')
        return response
    # new_book = {"name": request_data['name'],
    #             "price": request_data['price'],
    #             "isbn": isbn}
    book_replace(request_data['isbn'],request_data['name'],request_data['price'])
    response = Response("", status=204)
    return response


# UPDATE book using 'PATCH'
@app.route("/books/<int:isbn>", methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    # if not validBookObject(request_data):
    #     invalid_error_msg = {"error": "Invalid request",
    #                          "msg": "pass data like name ,price,isbn"}
    #     response = Response(dumps(invalid_error_msg), status=400, mimetype='application/json')
    #     return response

    if "price" in request_data:
        book_update_price(isbn, request_data['price'])
    if "name" in request_data:
        book_update_name(isbn, request_data['name'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# # DELETE BOOK
@app.route("/books/<int:isbn>",methods=['DELETE'])
def delete_book_isbn(isbn):
    if delete_book(isbn):
        response = Response(dumps("deleted sucessfully"), status=204)
        return response
    else:
        invalid_error_msg = {"error": "Invalid request",
                             "msg": "pass data like name ,price,isbn"}
        response = Response(dumps(invalid_error_msg), status=400, mimetype='application/json')
        return response


if __name__ == "__main__":
    app.run()
