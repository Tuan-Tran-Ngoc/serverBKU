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

db = client.MyProject
collection=db.schedule

@app.route('/schedule',methods=['GET'])
def fetch_schedule():
    itemp=request.query_string.decode()
    try:
        query_params = helper_module.parse_query_params(itemp)
        print(query_params)
        if query_params:
            todata=db.staff.aggregate([
                { "$match" : query_params },
                {
                "$lookup": {
                    "from": "schedule",
                    "localField": "staff_id",    
                    "foreignField": "staff_id", 
                    "as": "fromsStaffSchedule"
                    }
                },
                {
                    "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$fromsStaffSchedule", 0 ] }, "$$ROOT" ] } }
                },
                { 
                    "$project": { 
                        "fromsStaffSchedule": 0,
                        "_id":0
                    } 
                }
                ])
            df=list(todata)
            if len(df)>0:
                response=json.dumps(df, default=json_util.default)
                return response,201
            else:
                return "",404      
           
        else:
            if collection.find().count()>0:
                todata=collection.find({},{"_id":0}) 
                df=list(todata)
                response=json.dumps(df, default=json_util.default)      
                return response
            else:
                return jsonify([])
    except:
        return "",500
    