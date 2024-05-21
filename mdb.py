import flask
import pymongo
from flask import Flask
from pymongo import MongoClient



mongo_url = "mongodb+srv://kskkoushik135:LQCFjoGmTHFyIdRi@cluster0.zzxbiby.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

member = MongoClient(mongo_url)

db = member['Hiring_base']

username = db['username']

job_postings = db['job_postings']

def add_data(name , email , skills , questions ):
    username.insert_one({"name":name,"email":email,"skills":skills , 'proficiency' : [] ,'s_score':0 , 'questions':questions , 'logic_quest':[] ,'l_score':0 , 'reason_quest': [] , 'r_score':0 ,'verbal_quest':[] , 'v_score':0 , 'inter_chat':[]})
    return "data added";

def get_user_data(name):
    return username.find_one({'name':name})

def update_score(name, score):
    username.update_one({'name':name},{'$set':{'s_score':score}})
    return "score updated";

def update_l_score(name, score):
    username.update_one({'name':name},{'$set':{'l_score':score}})
    return "score updated";

def update_r_score(name, score):
    username.update_one({'name':name},{'$set':{'r_score':score}})
    return "score updated";

def update_v_score(name, score):
    username.update_one({'name':name},{'$set':{'v_score':score}})
    return "score updated";

def update_proficiency(name, proficiency):
    username.update_one({'name':name},{'$set':{'proficiency':proficiency}})
    return "proficiency updated";

def update_questions(name, questions):
    username.update_one({'name':name},{'$set':{'questions':questions}})
    return "questions updated";

def update_logic_questions(name, questions):
    username.update_one({'name':name},{'$set':{'logic_quest':questions}})
    return "l questions updated";

def update_reason_questions(name, questions):
    username.update_one({'name':name},{'$set':{'reason_quest':questions}})
    return "r questions updated";

def update_verbal_questions(name, questions):
    username.update_one({'name':name},{'$set':{'verbal_quest':questions}})
    return "v questions updated";

def update_inter_chat(name, chat):
    username.update_one({'name':name},{'$set':{'inter_chat':chat}})
    return "chat updated";


def get_all_data():
    return username.find()

def add_job_posting(job_title , job_description , job_skills):
    job_postings.insert_one({"job_title":job_title,"job_description":job_description,"job_skills":job_skills})
    return "job added";