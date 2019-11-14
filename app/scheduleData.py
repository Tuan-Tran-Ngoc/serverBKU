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
from io import StringIO
from flask import make_response,send_from_directory,abort,redirect,flash,url_for,Response
from werkzeug.utils import secure_filename

# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

db = client.MyProject
collection=db.schedule
collection1=db.demoinit

def converse(month,year):
    if (month+1)>12:
        month=1+(month-12)
        year=year+1
    else:
        month=month+1
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
                response=json.dumps(df, default=json_util.default)
                return response,201
            else:
                return "",404      
           
        else:
            if collection1.find().count()>0:
                todata=collection1.find({},{"_id":0}) 
                df=list(todata)
                response=json.dumps(df, default=json_util.default)      
                return response
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

UPLOAD_DIRECTORY = "./project/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.route('/schedule/export',methods=['GET'])
def export_schedule():
    a="1"
    b="4"
    c="2"
    df=general.read_mongo(collection1)
    df.to_csv('./project/api_uploaded_files/ROSTER_{0}_{1}_{2}.csv'.format(a,b,c), index=False)
    files = []
    # filename="demo.csv"
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)
    # return "complete"
    

UPLOAD_FOLDER = './project/api_uploaded_files'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkStaffExist(filename,pathFile):
    csvfile = open(pathFile, "r")
    reader = csv.DictReader( csvfile )
    for each in reader:
        if db.staff.find({"staff_id":each["staff_id"]}).count()>0:
            return False
    csvfile.close()
    return True

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    itemp=""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "No file part"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
            return "No selected file"
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            itemp=file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            pathFile='./project/api_uploaded_files/'+itemp
            if checkStaffExist(itemp,pathFile)==False:
                return dumps({'message' : 'duplicate staff_id'}),200
            else: general.saveInitFile(db.staff,pathFile)
            return redirect(url_for('upload_file',
                                    filename=filename))
        
    return dumps({'message' : 'SUCCESS'}),201
# @app.route("/getPlotCSV")
# def getPlotCSV():
#     with open("./project/api_uploaded_files/schedule.csv") as fp:
#         csv = fp.read()
#     a='toilatoi'
#     return Response(
#         csv,
#         mimetype="text/csv",
#         headers={"Content-disposition":
#                  "attachment; filename={0}.csv".format(a)})