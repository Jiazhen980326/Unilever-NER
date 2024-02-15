from flask import Flask, request
from flask_cors import CORS, cross_origin

from database import DB


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# import declared routes
import index_page
import input_page
import annotation_page
import new_entity

if __name__ == '__main__':
    app.run(debug=True)