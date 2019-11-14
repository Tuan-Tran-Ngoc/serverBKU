"""This is init module."""

from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)
from app import usersData,scheduleData,eventData,trainingData,offData

