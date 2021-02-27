db = {
    'user'     : 'sonic886',
    'password' : 'rlatmddn52!',
    'host'     : 'music-recommender-db.cpabptw8fwxo.us-east-2.rds.amazonaws.com',
    'port'     : '3306',
    'database' : 'music_recommender_db'
}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8" 