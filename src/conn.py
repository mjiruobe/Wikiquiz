from pymongo import MongoClient
# MongoDB Verbindung    
client = MongoClient('mongodb://mongo:27017/')
db = client['wikiQuiz']  # Datenbankauswahl
status_collection = db['status']  # Sammlungsauswahl
question_collection = db['questions']  # Sammlungsauswahls