from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_openai import ChatOpenAI as OpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
import random
from controller.prompt_builder import PromptBuilder
from conn import *

class Quiz:
    def __init__(self, wikiURL):
        self.wikiURL = wikiURL
        self._llm = OpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-3.5-turbo",
    )

    def _make_quiz_from_llm(self, llm, data):
        system = """
        Du bist ein Quizmaster und sollst vier Optionen bereitstellen. 
        Dir wird ein Fakt genannt und drei falsche Antworten musst du dir ausdenken.
        Mische die Antworten so, dass die richtige Antwort nicht immer an derselben Stelle steht.
        Stelle die passende Frage zu der richtigen Option.
        Gebe nicht an, welche der Optionen die richtige Antwort ist.

        Beispiel Eingabe:
        Frage nach der/die Verwandten von Barack Obama (Mensch). Die richtige Antwort ist Stanley Armour Dunham (Mensch).

        Beispiel Ausgabe:
        Wer ist der/die Verwandte von Barack Obama?
        1. Stan Lee
        2. Elon Musik
        3. Steve Jobs
        4. Stanley Armour Dunham
        """
        return self._ask_AI(llm, system, data)

    def _ask_AI(self, llm, system, data):
        template = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", "{data}"),
        ])
        return LLMChain(prompt=template, llm=llm).run({"data": data})

    def createQuiz(self):
        questions = PromptBuilder(self.wikiURL).build()
        while len(questions) > 0:
            question_index = random.randint(0, len(questions)-1)
            question = questions[question_index]
            correct_answer = question.correct_answer
            if correct_answer is None or question.prompt is None:
                del questions[question_index]
                continue
            quiz = self._make_quiz_from_llm(self._llm, question.prompt)
            if correct_answer in quiz:
                question.question = quiz.split("\n")[0]
                question.answers = quiz.split("\n")[-4:]
                question.answers = [answer.strip()[answer.index(".")+1:].strip() for answer in question.answers]
                question.correct_answer_id = [i for i, answer in enumerate(question.answers) if f"{correct_answer}" in answer]
                question.save()
                filter_condition = {"name": question.articleURL}

                # Definieren Sie die Aktualisierungsoperation
                update_operation = {"$set": {"state": "finish"}}

                # Führen Sie die Aktualisierung durch
                status_collection.update_one(filter_condition, update_operation)

                # Wenn Sie sicherstellen möchten, dass die Aktualisierung erfolgreich war, können Sie Folgendes tun:
                updated_status = status_collection.find_one(filter_condition)
                if updated_status:
                    print("Status erfolgreich aktualisiert:", updated_status)
                else:
                    print("Status konnte nicht aktualisiert werden.")
            del questions[question_index]