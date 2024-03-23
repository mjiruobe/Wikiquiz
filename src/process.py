from controller.quiz import Quiz
from conn import *
import time

def check_unfetched_status():
    while True:
        unfetched_status = status_collection.find_one({"state": "unfetched"})
        if unfetched_status:
            url = unfetched_status['name']
            quiz = Quiz(url)
            quiz.createQuiz()
        time.sleep(0.5)

if __name__ == "__main__":
    # Starten Sie die Überprüfung
    print("Starting processing unfetched questions script")
    check_unfetched_status()