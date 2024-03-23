import auth

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from conn import *
from fastapi.security.api_key import APIKey

app = FastAPI()
origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # MongoDB Verbindung
# client = MongoClient('mongodb://localhost:27017/')
# db = client['wikiQuiz']  # Datenbankauswahl
# status_collection = db['status']  # Sammlungsauswahl
# question_collection = db['questions']  # Sammlungsauswahl

# POST api/v1/requestarticles
@app.post("/api/v1/requestarticles")
async def request_articles(articles: List[str], api_key: APIKey = Depends(auth.get_api_key)):
    for article in articles:
        # Überprüfen, ob ein Statusobjekt mit dem Namen bereits existiert
        existing_status = status_collection.find_one({"name": article})
        if existing_status is None:
            # Wenn nicht vorhanden, ein neues Statusobjekt erstellen
            status_collection.insert_one({"name": article, "state": "unfetched"})

    return {"message": "successed"}

# GET api/v1/getarticlestate
@app.get("/api/v1/getarticlestate")
async def get_article_state(articles: List[str],api_key: APIKey = Depends(auth.get_api_key)):
    # Statusobjekte für die angegebenen Artikel abrufen
    article_states = []
    for article in articles:
        state_data = status_collection.find_one({"name": article})
        if state_data:
            article_states.append({"name": state_data["name"], "state": state_data["state"] })
        else:
            article_states.append({"name": state_data["name"], "state": "not found" })
    return {"data": article_states}

# GET api/v1/getquestions
@app.get("/api/v1/getquestions")
async def get_questions(articles: List[str], api_key: APIKey = Depends(auth.get_api_key)):
    questions = []
    for article in articles:
        # Fragen für den angegebenen Artikel abrufen
        article_questions = question_collection.find({"article": article})
        for question in article_questions:
            # Nur die relevanten Attribute zurückgeben
            questions.append({
                "article": question["article"],
                "question": question["question"],
                "answers": question["answers"],
                "correct_answer": question['correct_answer'],
                "questionId": question["questionId"]
            })
    return questions

# GET api/v1/getquestionresult
@app.get("/api/v1/getquestionresult")
async def get_question_result(questionId: int, api_key: APIKey = Depends(auth.get_api_key)):
    # Ergebnis für die Frage mit der angegebenen ID abrufen
    question_result = question_collection.find_one({"questionId": questionId})
    if question_result:
        return {"questionId": question_result["questionId"], "correct_answer": question_result["correct_answer"]}
    else:
        raise HTTPException(status_code=404, detail="Question result not found")