from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import pymysql
import numpy as np
import pandas as pd
import json
from models.songAnalysisModel import SongAnalysis
from models.songRecommenderModel import SongRecommender

def db_connector(value):
    with open('database.json') as json_file:
        dbset = json.load(json_file)
    db_connection_str = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(dbset['user'], dbset['password'], dbset['host'], dbset['port'], dbset['database'])
    sql = "SELECT id, song_id, artists, name FROM original_table WHERE name='{}';".format(value)
    db_connection = create_engine(db_connection_str)
    result = pd.read_sql(sql, con=db_connection)
    return result

def show_result(sqlStr):
    with open('database.json') as json_file:
        dbset = json.load(json_file)
    db_connection_str = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(dbset['user'], dbset['password'], dbset['host'], dbset['port'], dbset['database'])
    sql = "SELECT id, song_id, artists, name FROM original_table WHERE song_id IN {};".format(sqlStr)
    db_connection = create_engine(db_connection_str)
    result = pd.read_sql(sql, con=db_connection)
    return result

def make_sql_IN_syntex(idList):
    sqlStr = "("
    for i in range(len(idList) - 1):
        sqlStr += "'{}', ".format(idList[i])
    sqlStr += "'{}')".format(idList[-1])
    return sqlStr

def drop_duplicated_id_and_name(data):
    return data.drop_duplicates(['id']).drop_duplicates(['name'])

def merge_responses(recommendedData, analysisData):
    # analysisData to dict
    analysisDataElement = dict(zip(range(1, len(analysisData) + 1), analysisData))
    analysisToDict = analysisDataElement
    #analysisToDict = {'analysis' : analysisDataElement}

    # recommendedData to dict
    recommendedData = recommendedData.to_json(orient='records')
    recommendedResultJson = json.loads(recommendedData)
    recommendedResultJson.append(analysisToDict)

    # dict to json
    responseData = json.dumps(recommendedResultJson)
    return responseData

app = Flask(__name__)

@app.route('/api/musicL')
def index():
    connectedResult = db_connector()
    JsonResult = connectedResult.to_json(orient='records')
    return JsonResult

@app.route('/api/musicL', methods=['POST'])
def post():
    value = request.form['songName']
    result = db_connector(value)
    textJson = result.to_json(orient='records')
    return textJson

@app.route('/api/musicL_', methods=['POST'])
def post_():
    value = request.form['songId']
    
    # get analysis data
    analysis = SongAnalysis(str(value))
    analysisResult = analysis.ExplaneFeatures()

    # get recommend data
    recommender = SongRecommender((str(value)))
    recommendedResult = list(recommender.get_recommendations())
    sqlStr = make_sql_IN_syntex(recommendedResult)
    recommendedResult = show_result(sqlStr)
    recommendedResult = drop_duplicated_id_and_name(recommendedResult)

    # merge data
    responseData = merge_responses(recommendedResult,analysisResult)
    return responseData

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port="8000")
    app.run(debug=True)