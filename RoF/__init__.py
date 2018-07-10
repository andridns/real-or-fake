import os
import csv
import smtplib
import random
import numpy as np
import pandas as pd
from pathlib import Path
from flask import Flask, redirect, render_template, request
from flask_restful import Resource, Api
from flask.json import jsonify
import sqlite3

app = Flask(__name__)
api = Api(app)

# PATH = '/var/www/RoF/RoF/' # server
PATH = 'C:/Users/adsasmita/Desktop/RoF/RoF/' # local
cols = ['index','author','comment','line','truth']
DB_PATH = PATH+"db/"
    
@app.route("/")
def index():
    return render_template("index.html")
    
class Popular_Magazine(Resource):
    def get(self, idx):
        conn = sqlite3.connect(DB_PATH+'popMag.db')
        qstr = f"select * from popMag WHERE id={idx}"
        query = conn.execute(qstr).fetchall()[0]
        result = dict(zip(cols,list(query)))
        return jsonify(result)

class Kompas(Resource):
    def get(self, idx):
        conn = sqlite3.connect(DB_PATH+'kompas.db')
        qstr = f"select * from kompas WHERE id={idx}"
        query = conn.execute(qstr).fetchall()[0]
        result = dict(zip(cols,list(query)))
        return jsonify(result)

class Labels(Resource):
    def get(self):
    	result = {'kompas':{'shape':2090,
    						'source':"https://www.youtube.com/user/KompasTVNews"},
    			  'pop_mag':{'shape':4444,
    			  			 'source':"https://www.youtube.com/user/PopularMagazine"}}
    	return jsonify(result)

api.add_resource(Popular_Magazine, '/labels/pop_mag/<idx>')
api.add_resource(Kompas, '/labels/kompas/<idx>')
api.add_resource(Labels, '/labels_meta/')

if __name__ == "__main__":
    app.run(debug=True)
