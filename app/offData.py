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

csvOffPath = "./data/off_schedule.csv"

db = client.MyProject
collection=db.off

@app.route("/off", methods=['GET'])
def fetch_off():
    if ((collection.find().count()>0) is False):
        general.saveInitFile(collection ,csvOffPath)
    return general.fetch(collection)

# @app.route('/off',methods=['POST'])
# def create_event():
#     return general.create(collection)
