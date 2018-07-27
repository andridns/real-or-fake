import os
import numpy as np
import pandas as pd
from flask import Flask, redirect, render_template, request
from flask_restful import Resource, Api
from flask.json import jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
api = Api(app)

# PATH = '/var/www/RoF/RoF/' # server
PATH = 'C:/Users/adsasmita/Desktop/RoF/RoF/' # local
cols = ['index','line','truth']
DB_PATH = PATH+"db/"
QUIZ_META = {'kompas':{
						'name': "KompasTV's Youtube",
						'shape':23954,
						'source':"https://www.youtube.com/user/KompasTVNews"
						},
			'copypasta_twitch':{
						'name': "Twitch Copypastas",
						'shape':3928,
						'source':"https://www.twitchquotes.com/copypastas"
						},
			'najwa':{
						'name': "Najwa Shihab's Youtube",
						'shape':32390,
						'source':"https://www.youtube.com/channel/UCo8h2TY_uBkAVUIc14m_KCA"
						},
			'pop_mag':{
						'name': "PopMag Indonesia's Youtube",
						'shape':4444,
						'source':"https://www.youtube.com/user/PopularMagazine"
						},
			'bulldog':{
						'name': "AdmiralBulldog's Youtube",
						'shape':38256,
						'source':"https://www.youtube.com/channel/UCk8ZIMJxSO9-pUg7xyrnaFQ"
						}
			}

def timenow(): return datetime.utcnow()

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/append_quiz', methods=['POST'])
def append_quiz():
    dt = timenow()
    conn = sqlite3.connect(DB_PATH+'Records.db')
    conn.isolation_level = None
    d = conn.cursor()
    rows = request.json['data']
    for row in rows:
        user_name, dataset, line_index, line, correct = row['user_name'], row['dataset'], row['index'], row['line'], row['correct']
        d.execute("""INSERT INTO Records (Datetime, UserName, Dataset, LineIndex, Line, Correct) VALUES (?,?,?,?,?,?)""", (dt, user_name, dataset, line_index, line, correct))
    conn.close()
    return ""

class Labels(Resource):
	def get(self, dataset, idx):
		conn = sqlite3.connect(DB_PATH+f"{dataset}.db")
		qstr = f"select * from {dataset} WHERE id={idx}"
		query = conn.execute(qstr).fetchall()[0]
		result = dict(zip(cols,list(query)))
		return jsonify(result)

class Leaderboards(Resource):
    def get(self, dataset):
        conn = sqlite3.connect(DB_PATH+'Records.db')
        df = pd.read_sql_query("SELECT * FROM Records", conn)
        df.Datetime = pd.to_datetime(df.Datetime)
        df = df[df.Dataset == dataset]
        res = df.groupby(['Datetime','UserName'])['Correct'].mean().reset_index().sort_values(by=['Correct','Datetime'],ascending=False)[:3]
        res.Datetime = res.Datetime.dt.strftime('%B %d, %Y, %r')
        res.Correct = (res.Correct*100).astype(str) + ' %'
        res.columns = ['Timestamp','Player','Score']
        res.reset_index(inplace=True, drop=True)
        res['Rank'] = res.index +1
        res['Dataset'] = dataset
        resdict = res.to_dict('records')
        #resdict['Dataset'] = dataset
        return jsonify(resdict)
    
class Labels_Meta(Resource):
	def get(self, dataset):
		return jsonify(QUIZ_META[dataset])

api.add_resource(Labels, '/labels/<dataset>/<idx>')
api.add_resource(Labels_Meta, '/labels_meta/')
api.add_resource(Leaderboards, '/leaderboards/<dataset>')


class Quiz_ID(Resource):
    def get(self, dataset):
        quiz_ids = {
                    'dataset': dataset,
                    'shape': QUIZ_META[dataset]['shape'],
                    'ids': np.random.randint(0,QUIZ_META[dataset]['shape'], size=20).tolist()
                    }
        return jsonify(quiz_ids)

class Line(Resource):
    def get(self, dataset, idx):
        conn = sqlite3.connect(DB_PATH+f"{dataset}.db")
        qstr = f"select line from {dataset} WHERE id={idx}"
        line = conn.execute(qstr).fetchall()[0][0]
        result = {"line":line}
        return jsonify(result)

class Truth(Resource):
    def get(self, dataset, idx):
        conn = sqlite3.connect(DB_PATH+f"{dataset}.db")
        qstr = f"select true from {dataset} WHERE id={idx}"
        truth = conn.execute(qstr).fetchall()[0][0]
        result = {"truth":truth}
        return jsonify(result)

class Guess(Resource):
    def get(self, dataset, idx, guess):
        conn = sqlite3.connect(DB_PATH+f"{dataset}.db")
        qstr = f"select true from {dataset} WHERE id={idx}"
        truth = conn.execute(qstr).fetchall()[0][0]
        result = {"result": int(truth)==int(guess)}
        return jsonify(result)

api.add_resource(Quiz_ID, '/api/get_ids/<dataset>')
api.add_resource(Line, '/api/line/<dataset>/<idx>/')
api.add_resource(Truth, '/api/truth/<dataset>/<idx>/')
api.add_resource(Guess, '/api/guess/<dataset>/<idx>/<guess>')










if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(9001), debug=True)
