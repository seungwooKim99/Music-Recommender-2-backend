from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import pymysql
import numpy as np
import pandas as pd
import json

def db_connector(value):
    with open('database.json') as json_file:
        dbset = json.load(json_file)
    db_connection_str = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(dbset['user'], dbset['password'], dbset['host'], dbset['port'], dbset['database'])
    sql = "SELECT id, song_id, artists, name FROM original_table WHERE name='{}';".format(value)
    db_connection = create_engine(db_connection_str)
    result = pd.read_sql(sql, con=db_connection)
    return result

app = Flask(__name__)

@app.route('/api/musicL')
def index():
    a = db_connector()
    # a = pd.DataFrame(a)
    testJson = a.to_json(orient='records')
    return testJson

@app.route('/api/musicL', methods=['POST'])
def post():
    value = request.form['songName']
    print(value)
    result = db_connector(value)
    print(result)
    textJson = result.to_json(orient='records')
    return textJson

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port="8000")
    app.run(debug=True)