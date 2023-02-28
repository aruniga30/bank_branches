#import libraries
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS
from flask import Flask , render_template , request , redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bot_sqlite.sqlite3"

db = SQLAlchemy(app)
app.app_context().push()
api = Api(app)
CORS(app)

#Table creation
class Bank(db.Model):
    ifsc = db.Column(db.String, primary_key=True)
    bank_id = db.Column(db.Integer)
    branch = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    district = db.Column(db.String)
    state = db.Column(db.String)
    bank_name = db.Column(db.String)

import sqlite3
class SEARCH(Resource):
    def get(self):
        conn = sqlite3.connect(r"C:\Users\Aruniga\Desktop\Bot\instance\bot_sqlite.sqlite3")
        #extracting the table
        all_posts = conn.execute('SELECT * FROM bank').fetchall()
        conn.close()
        #extracting query
        query = request.args.get('q').upper()
        #extracting limit
        limit = int(request.args.get('limit'))
        #extracting offset
        offset = int(request.args.get('offset'))
        spec = []
        for i in all_posts:
            f=0
            for j in range(2,8):
                if i[j] and query in i[j]:
                    f=1
            if f:
                spec.append(i)

    
        obj = spec[(offset):(offset+limit)]
        l=[]
        for i in obj:
            l.append((i[0],{"ifsc":i[0],
                              "bank_id":i[1],
                              "branch":i[2],
                              "address":i[3],
                              "city":i[4],
                              "district":i[5],
                              "state":i[6],
                              "bank_name":i[7]
                              }))     
        l.sort()
        temp=[]
        for i in l:
           temp.append(i[1])
        return {
            "branches":temp
        }

class BRANCH(Resource):
    def get(self):
        conn = sqlite3.connect(r"C:\Users\Aruniga\Desktop\Bot\instance\bot_sqlite.sqlite3")
        posts = conn.execute('SELECT * FROM bank').fetchall()
        conn.close()
        query = request.args.get('q').lower()
        limit = int(request.args.get('limit'))
        offset = int(request.args.get('offset'))
        ind = []
        
        for i in posts:
            f=0
            for j in range(2,8):
                if i[j] and query in i[j].lower():
                    f=1
            if f:
                ind.append(i)

        obj = ind[(offset):(offset+limit)]
        l=[]
        for i in obj:
            l.append((i[0],{"ifsc":i[0],
                              "bank_id":i[1],
                              "branch":i[2],
                              "address":i[3],
                              "city":i[4],
                              "district":i[5],
                              "state":i[6],
                              }))          
            
        l.sort(reverse=True)
        temp=[]
        for i in l:
           temp.append(i[1])
        return {
            "branches":temp
        }
    
api.add_resource(SEARCH,'/api/search')
api.add_resource(BRANCH,'/api/branch')

if _name_ == '_main_':
    app.run(debug=True,port=5050)