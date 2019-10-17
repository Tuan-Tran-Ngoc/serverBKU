from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import ast,imp,os
import csv, json
import pandas as pd
from bson import json_util
import bson
from app import functionGeneral as general

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

csvTrainingPath = "./data/training.csv"

db = client.MyProject
collection=db.training

@app.route("/training", methods=['GET'])
def fetch_training():
    if ((collection.find().count()>0) is False):
        general.saveInitFile(collection ,csvTrainingPath)
    return general.fetch(collection)

@app.route('/training',methods=['POST'])
def create_training():
    return general.create(collection)


