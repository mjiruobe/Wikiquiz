from pymongo import MongoClient
import os
import urllib.parse
# MongoDB Verbindung    
client = MongoClient('mongodb://%s:%s@mongo:27017/' % (urllib.parse.quote_plus(os.environ.get('MONGO_USER')), urllib.parse.quote_plus(os.environ.get('MONGO_PASSWORD'))))
db = client['wikiQuiz']  # Datenbankauswahl
status_collection = db['status']  # Sammlungsauswahl
question_collection = db['questions']  # Sammlungsauswahls