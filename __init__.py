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

PATH = '/var/www/RoF/RoF/'
cols = ['index','author','comment','line','truth']
DB_PATH = PATH+"rnn.db"
# CSV_PATH = PATH+'database.csv'
# DATA_PATH = PATH+'pop_mag.csv'
# COLS = ['Name','Line','Guess','Truth','Correct']
# df = pd.read_csv(DATA_PATH, index_col=0)
# author, user, line, truth = df.iloc[random.randint(0, df.shape[0])].values
    
@app.route("/")
def index():
    return render_template("index.html")
    
class Youtube_Comment(Resource):
    def get(self, idx):
        conn = sqlite3.connect(DB_PATH)
        qstr = f"select * from popMag WHERE id={idx}"
        query = conn.execute(qstr).fetchall()[0]
        result = dict(zip(cols,list(query)))
        
        return jsonify(result)
    
api.add_resource(Youtube_Comment, '/ytcmt/<idx>') # Route_3

if __name__ == "__main__":
    app.run(debug=True)
