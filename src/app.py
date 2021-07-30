from flask import Flask, jsonify, request,redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from mysql.connector import Error

import credentials as credentials
import validators
import json
import mysql.connector
import string
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/gds_assessment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

# Model Definition
class UrlMapTab(db.Model):
    __tablename__ = "url_map_tab"

    id = db.Column(db.Integer,primary_key=True, auto_increment=True)
    shortened_url = db.Column(db.String)
    original_url = db.Column(db.String)

    # sets the properties (of itself) when created
    def __init__ (self, shortened_url, original_url):
        self.shortened_url = shortened_url
        self.original_url = original_url

    # representation of data in json format
    def json(self):
        return {"id": self.id, "shortened_url": self.shortened_url, "original_url": self.original_url}

def createUniqueID(n):
    return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k = n))


@app.route("/api/shorten_url", methods=["POST"])
def shortern_url():
    # get the url from the request body
    data = request.json
    original_url = data["original_url"]

    # Add http if it does not contain http (TinyURL does this)
    if "http" not in original_url:
        original_url = "http://" + original_url

    # Check if original url is valid
    if not (validators.url(original_url)):
        return jsonify({"message" : "invalid URL", "original_url": original_url})

    # check if the url exists
    # Assumption: https would equate to http if it has the same url (less the host) 
    record = UrlMapTab.query.filter_by(original_url=original_url).first()
    # To ensure that we are not missing records because of http and https
    if not record:
        # check for http version if its https
        if original_url[0:5] == "https":
            http_original_url = "http" + original_url[5::]
            record = UrlMapTab.query.filter_by(original_url=http_original_url).first()
        # check for https version if its http
        elif original_url[0:4] == "http":
            http_original_url = "https" + original_url[4::]
            record = UrlMapTab.query.filter_by(original_url=http_original_url).first()

    # If record exists already 
    if record:
        return jsonify({"message" : "URL already shortened before", "original_url":record.original_url, "shortened_url": record.shortened_url})

    # create new record if not exists
    new_url_map_data = UrlMapTab(shortened_url= "", original_url= original_url)
    url_alias = createUniqueID(10) # hardcoded 10 in length
    # check if id exists before
    while(UrlMapTab.query.filter_by(shortened_url=url_alias).first()):
        url_alias = createUniqueID(7)

    # update new id
    new_url_map_data.shortened_url = url_alias

    # ready to add into db     
    try:
        db.session.add(new_url_map_data)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": "create url_map_tab record error."}), 500

    return jsonify({"message": "Successfully shortened URL", "original_url":new_url_map_data.original_url, "shortened_url": new_url_map_data.shortened_url}), 200

@app.route("/api/<string:uid>")
def get_original_url(uid):
    record = UrlMapTab.query.filter_by(shortened_url=uid).first()
    if record == None:
        return jsonify({"message": "invalid uid"}), 500 
    
    return jsonify({"original_url": record.original_url}), 200
    # return redirect(record.original_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)