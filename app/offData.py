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
    itemp=request.query_string.decode()
    try:
        query_params = helper_module.parse_query_params(itemp)
        if query_params:
            todata=db.staff.aggregate([
                { "$match" : query_params },
                {
                "$lookup": {
                    "from": "off",
                    "localField": "staff_id",    
                    "foreignField": "staff_id", 
                    "as": "fromsStaffOff"
                    }
                },
                {
                    "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$fromsStaffOff", 0 ] }, "$$ROOT" ] } }
                },
                { 
                    "$project": { 
                        "fromsStaffOff": 0,
                        "_id":0
                    } 
                }
                ])
            df=list(todata)
            if len(df)>0:
                # response=json.dumps(df, default=json_util.default)
                return jsonify({'ok': query_params, 'data': df}),201
            else:
                return "",404      
           
        else:
            if collection.find().count()>0:
                todata=collection.find({},{"_id":0}) 
                df=list(todata)
                # response=json.dumps(df, default=json_util.default)      
                return jsonify({'ok': True, 'data': df})
            else:
                return jsonify([])
    except:
        return "",500

# @app.route('/off',methods=['POST'])
# def create_event():
#     return general.create(collection)
