import flask
import pymongo
from flask import Flask
from pymongo import MongoClient



mongo_url = "mongodb+srv://kskkoushik135:LQCFjoGmTHFyIdRi@cluster0.zzxbiby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

member = MongoClient(mongo_url)

db = member['Hiring_base']

username = db['username']

def add_data(name , email , skills , questions):
    username.insert_one({"name":name,"email":email,"skills":skills , 'score':0 , 'questions':questions})
    return "data added";

def get_user_data(name):
    return username.find_one({'name':name})

def update_score(name, score):
    username.update_one({'name':name},{'$set':{'score':score}})
    return "score updated";
