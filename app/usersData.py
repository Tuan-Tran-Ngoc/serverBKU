from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import ast,imp,os
import csv, json
import pandas as pd
from bson import json_util
from app import functionGeneral as general

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

csvSchedulePath = "./data/schedule.csv"
csvStaffPath = "./data/staff.csv"

# Select the database
db = client.MyProject    
collection=db.staff

@app.route('/')
def index():
    if (db.schedule.find().count()>0):
        if(db.staff.find().count()>0):
            return "database created earlier"
        else:
            general.saveInitFile(db.staff,csvStaffPath)
            return "New database is created"
    else:
        general.saveInitFile(db.schedule,csvSchedulePath)
        return index()

@app.route('/staff',methods=['POST'])
def create_user():
    return general.create(collection)

@app.route("/staff/<id>", methods=['DELETE','PUT'])
def remove_updateUser(id):
    if request.method == 'DELETE':
        return general.delete(collection,id)
    else:
        return general.update(collection,id)

@app.route("/staff", methods=['GET'])
def fetch_users():
    return general.fetch(collection)

