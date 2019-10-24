from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import ast,imp,os
import csv, json
import pandas as pd
from bson import json_util
import datetime
from bson.objectid import ObjectId

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# Select the database
db = client.MyProject    

def saveInitFile(collection,pathFile):
    csvfile = open(pathFile, "r")
    reader = csv.DictReader( csvfile )
    db.segment.drop()
    for each in reader:
        each["create_at"]=each["update_at"]=datetime.datetime.now()
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
        for x in body:
            x["create_at"]=datetime.datetime.now()
            x["update_at"]=datetime.datetime.now()
        record_created=collection.insert(body)
        if isinstance(record_created,list):
            return jsonify([str(v) for v in record_created]),201
        else:
            return jsonify(str(record_created)),201
            
    except:
        return "",500

def delete(collection,id):
    try:
        delete_user = collection.delete_one({'_id': ObjectId(id)})
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
        if collection.find({'_id': ObjectId(id)}).count()>0:
            copy=body[0]
            copy["update_at"]=datetime.datetime.now()
            records_updated = collection.update({'_id': ObjectId(id)},{"$set":body[0]})
        # records_updated.modified_count error
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
            records_fetched = collection.find(query_params,{"_id":0})
            if records_fetched.count() > 0:
                df=list(records_fetched)
                return jsonify({'ok': query_params, 'data': df}),202
            else:
                return "", 404
        else:
            if collection.find().count()>0:
                todata=collection.find({},{"_id":0}) 
                df=list(todata)
                # response=json.dumps(df, default=json_util.default)      
                return jsonify({'ok': True, 'data': df}),202
            else:
                return jsonify([]),404
    except:
        return "", 500


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def createScheduleInit(month,year,month1,year1,collection,c1,itemp,staff,staff_id):
    list=["1","-1","-1","-1","0","0","0","0"]
    if itemp==0:
        collection.insert_one({"staff_id" : staff_id})
        for result in perdelta(datetime.date(int(year),int(month),21), datetime.date(int(year1),int(month1),21), datetime.timedelta(days=1)):
            collection.update_one(
            { "staff_id": staff_id},
            {   
                "$set": {str(result):list[c1]}
            }
            )
            staff=staff_id
            if (c1<7): c1=c1+1
            else: c1=0
        collection.update_one(
        { "staff_id": staff_id},
        {   
            "$set": {"create_at":datetime.datetime.now(),"update_at":datetime.datetime.now()}
        }
        )
    else:
        copy=collection.find_one({"staff_id":staff},{"_id":0})
        collection.insert_one(copy)
        collection.update_one(
        { "staff_id": staff},
        {   
            "$set": {"staff_id": staff_id}
        }
        )          
    itemp=1

