"""This module is to configure app to connect with database."""
from pymongo import MongoClient
local=MongoClient('localhost', 27017)
DEBUG = True
client = MongoClient("mongodb+srv://tuantran:chinhlatoi1@cluster0-gtudj.mongodb.net/test?retryWrites=true&w=majority")