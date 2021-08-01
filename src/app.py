from flask import Flask, jsonify, request,redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask_pymongo import pymongo

import credentials as credentials
import validators
import json
import mysql.connector
import string
import random

app = Flask(__name__)
CONNECTION_STRING = credentials.MONGO_CONNECTION_URL
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('gds_assessment')
url_map_tab = pymongo.collection.Collection(db, 'url_map_tab')


CORS(app)
db = SQLAlchemy(app)

def createUniqueID(n):
    return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k = n))


@app.route("/api/shorten_url", methods=["POST"])
def shorten_url():
    try:
        # get the url from the request body
        data = request.json
        print(data)
        original_url = data["original_url"]

        # Add http if it does not contain http (TinyURL does this)
        if "http" not in original_url:
            original_url = "http://" + original_url

        # Check if original url is valid
        if not (validators.url(original_url)):
            return jsonify({"success" : False, "message" : "invalid URL", "original_url": original_url}), 400

        # check if the url exists
        # Assumption: https would equate to http if it has the same url (less the host) 
        query = {"original_url" : original_url}
        record = url_map_tab.find_one(query)
        # To ensure that we are not missing records because of http and https
        if not record :
            # check for http version if its https
            if original_url[0:5] == "https":
                http_original_url = "http" + original_url[5::]
                query = {"original_url" : http_original_url}
                record = url_map_tab.find_one(query)
            # check for https version if its http
            elif original_url[0:4] == "http":
                http_original_url = "https" + original_url[4::]
                query = {"original_url" : http_original_url}
                record = url_map_tab.find_one(query)

        # If record exists already 
        if record:
            print(record)
            return jsonify({"success":False,"message" : "URL already shortened before", "original_url":record["original_url"], "shortened_url": record["shortened_url"]}), 400

        url_alias = createUniqueID(10) # hardcoded 10 in length
        # check if alias exists before
        query = {"shortened_url" : url_alias}
        record = url_map_tab.find_one(query)
        while(record):
            url_alias = createUniqueID(7)
            record = url_map_tab.find_one(query)
        
       
        # ready to add into db     
        try:
            # create new record
            new_url_map_data = {"shortened_url": url_alias, "original_url": original_url}
            url_map_tab.insert_one(new_url_map_data)
        except Exception as e:
            print(e)
            return jsonify({"success":False,"message": "create url_map_tab record error."}), 500

        return jsonify({"success":True,"message": "Successfully shortened URL", "original_url":new_url_map_data["original_url"], "shortened_url": new_url_map_data["shortened_url"]}), 200
    except Exception as e:
        return jsonify({"success": False, "message": e})

@app.route("/api/<string:uid>")
def get_original_url(uid):
    record = url_map_tab.find_one({"shortened_url":uid})
    if record == None:
        return jsonify({"message": "invalid uid"}), 500 
    
    # return jsonify({"original_url": record.original_url}), 200
    return redirect(record["original_url"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)