"""This is init module."""

from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from app import usersData,scheduleData,eventData,trainingData,offData

