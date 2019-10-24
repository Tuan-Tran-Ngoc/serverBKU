from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import ast,imp,os
import csv, json
import pandas as pd
from bson import json_util
import bson,datetime
from app import functionGeneral as general

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

db = client.MyProject
collection=db.schedule
collection1=db.demoinit

def converse(month,year):
    if (month+4)>13:
        month=3+(month-12)
        year=year+1
    else:
        month=month+3
    return month,year

@app.route('/schedule',methods=['GET'])
def fetch_schedule():
    itemp=request.query_string.decode()
    try:
        query_params = helper_module.parse_query_params(itemp)
        if query_params:
            todata=db.staff.aggregate([
                { "$match" : query_params },
                {
                "$lookup": {
                    "from": "demoinit",
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
                # response=json.dumps(df, default=json_util.default)
                return jsonify({'ok': query_params, 'data': df}),201
            else:
                return "",404      
           
        else:
            if collection1.find().count()>0:
                todata=collection1.find({},{"_id":0}) 
                df=list(todata)
                # response=json.dumps(df, default=json_util.default)      
                return jsonify({'ok': True, 'data': df})
            else:
                return jsonify([])
    except:
        return "",500

@app.route('/schedule/<month>/<year>',methods=['GET'])
def schedule(month,year): 
    itemp=itemp2=itemp3=itemp4=0
    c1=0
    c2=7
    c3=6
    c4=5
    staff=staff2=staff3=staff4=""
    month1,year1=converse(int(month),int(year))
    for x in db.staff.find():
        if x["crew"]=="1":
            general.createScheduleInit(month,year,month1,year1,collection1,c1,itemp,staff,x["staff_id"])
        elif x["crew"]=="2":
            general.createScheduleInit(month,year,month1,year1,collection1,c2,itemp2,staff2,x["staff_id"])
        elif x["crew"]=="3":
            general.createScheduleInit(month,year,month1,year1,collection1,c3,itemp3,staff3,x["staff_id"])
        elif x["crew"]=="4":
            general.createScheduleInit(month,year,month1,year1,collection1,c4,itemp4,staff4,x["staff_id"])
        
    return "1"