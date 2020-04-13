from flask import Flask

from settings import *
from BookModel import *

@app.route("/")
def hello_world():
    return 'Hello World!'

@app.route("/<name>")
def hello_name(name):
    return "Hello" + name

if __name__ == "__main__":
   app.run()



