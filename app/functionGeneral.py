from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import ast,imp,os
import csv, json
import pandas as pd
from bson import json_util

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# Select the database
db = client.MyProject    

def saveInitFile(collection,pathFile):
    csvfile = open(pathFile, "r")
    reader = csv.DictReader( csvfile )
    db.segment.drop()
    for each in reader:
        collection.insert_one(each)
    csvfile.close()

def joinStaffProfile():
    collection=db.staff
    todata=db.profile.aggregate([{
        "$lookup": {
            "from": "staff",
            "localField": "staff_id",    
            "foreignField": "staff_id", 
            "as": "fromsStaffProfile"
            }
        },
        {
            "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$fromsStaffProfile", 0 ] }, "$$ROOT" ] } }
        },
        { 
            "$project": { 
                "fromsStaffProfile": 0
            } 
        }
        ])
        # db.logout()    
    df=list(todata)
    response='{"data":'+json.dumps(df, default=json_util.default)+'}'      
       
    return response

def create(collection):
    try:
        try:
            body=ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "",400
        record_created=collection.insert(body)
        if isinstance(record_created,list):
            return jsonify([str(v) for v in record_created]),201
        else:
            return jsonify(str(record_created)),201
            
    except:
        return "",500

def delete(collection,id):
    try:
        delete_user = collection.delete_one({"id": id})
        if delete_user.deleted_count > 0 :
            return "", 204
        else:
            return "", 404
    except:
        return "", 500

def update(collection,id):
    try:
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "", 400
        records_updated = collection.update({"id": id},body)
        if records_updated.modified_count > 0:
            return "", 200
        else:
            return "", 404
    except:
        return "", 500

def fetch(collection):
    itemp=request.query_string.decode()
    try:
        query_params = helper_module.parse_query_params(itemp)
        if query_params:
            records_fetched = collection.find(query_params)
            if records_fetched.count() > 0:
                return dumps(records_fetched),202
            else:
                return "", 404
        else:
            if collection.find().count() > 0:
                return dumps(collection.find())
            else:
                return jsonify([])
    except:
        return "", 500