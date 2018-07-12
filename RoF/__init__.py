import os
import pandas as pd
from flask import Flask, redirect, render_template, request
from flask_restful import Resource, Api
from flask.json import jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
api = Api(app)

PATH = '/var/www/RoF/RoF/' # server
# PATH = 'C:/Users/adsasmita/Desktop/RoF/RoF/' # local
cols = ['index','line','truth']
DB_PATH = PATH+"db/"

def timenow(): return datetime.utcnow()
# def dt2id(dt): return int((dt-datetime(2018,7,11)).total_seconds()*10000)
# def id2dt(dtid): return datetime(2018,7,11)+timedelta(seconds=dtid/10000)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/append_quiz', methods=['POST'])
def append_quiz():
    dt = timenow()
    # dtid = dt2id(dt)
    conn = sqlite3.connect(DB_PATH+'Records.db')
    d = conn.cursor()
    rows = request.json['data']
    for row in rows:
        user_name, dataset, line_index, line, correct = \
            row['user_name'], row['dataset'], row['index'], row['line'], row['correct']
        d.execute('INSERT INTO Records (Datetime, UserName, Dataset, LineIndex, Line, Correct)'
                  'VALUES (?,?,?,?,?,?)', (dt, user_name, dataset, line_index, line, correct))
    conn.commit()
    conn.close()
    resp = {"append_quiz":True}
    print(resp)
    return jsonify(resp)

class Labels(Resource):
    def get(self, dataset, idx):
        conn = sqlite3.connect(DB_PATH+f"{dataset}.db")
        qstr = f"select * from {dataset} WHERE id={idx}"
        query = conn.execute(qstr).fetchall()[0]
        result = dict(zip(cols,list(query)))
        return jsonify(result)
    
class Labels_Meta(Resource):
    def get(self):
    	result = {'kompas':{'name': "KompasTV's Youtube",
    						'shape':23954,
    						'source':"https://www.youtube.com/user/KompasTVNews"},
    			  'najwa':{'name': "Najwa Shihab's Youtube",
    			  		   'shape':32390,
    			  		   'source':"https://www.youtube.com/channel/UCo8h2TY_uBkAVUIc14m_KCA"},
    			  'pop_mag':{'name': "PopMag Indonesia's Youtube",
    			  			 'shape':4444,
    			  			 'source':"https://www.youtube.com/user/PopularMagazine"},
    			  'bulldog':{'name': "AdmiralBulldog's Youtube",
    			  			 'shape':38256,
    			  			 'source':"https://www.youtube.com/channel/UCk8ZIMJxSO9-pUg7xyrnaFQ"}}
    	return jsonify(result)

api.add_resource(Labels, '/labels/<dataset>/<idx>')
api.add_resource(Labels_Meta, '/labels_meta/')

if __name__ == "__main__":
    app.run(debug=True)



# class Popular_Magazine(Resource):
#     def get(self, idx):
#         conn = sqlite3.connect(DB_PATH+'pop_mag.db')
#         qstr = f"select * from popMag WHERE id={idx}"
#         query = conn.execute(qstr).fetchall()[0]
#         result = dict(zip(cols,list(query)))
#         return jsonify(result)

# class Kompas(Resource):
#     def get(self, idx):
#         conn = sqlite3.connect(DB_PATH+'kompas.db')
#         qstr = f"select * from kompas WHERE id={idx}"
#         query = conn.execute(qstr).fetchall()[0]
#         result = dict(zip(cols,list(query)))
#         return jsonify(result)

# api.add_resource(Popular_Magazine, '/labels/pop_mag/<idx>')
# api.add_resource(Kompas, '/labels/kompas/<idx>')