from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import ast,imp,os
import csv, json
import pandas as pd
from bson import json_util
import bson,click
from app import functionGeneral as general

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

csvEventPath = "./data/event.csv"

db = client.MyProject
collection=db.event

@app.route("/event", methods=['GET'])
def fetch_event():
    if ((collection.find().count()>0) is False):
        general.saveInitFile(collection ,csvEventPath)
    return general.fetch(collection)

@app.route('/event',methods=['POST'])
def create_event():
    return general.create(collection)

@app.route('/event/upload/<file_name>',methods=['PUT'])
def upload():
    return ""

@app.route("/event/<id>", methods=['DELETE','PUT'])
def remove_updateEvent(id):
    if request.method == 'DELETE':
        return general.delete(collection,id)
    else:
        return general.update(collection,id)