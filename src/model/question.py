from typing import Union
from conn import *

class Question:
  articleURL: str
  question: str
  correct_answer: Union[str, None]
  correct_answer_id: Union[int, None]
  answer_options: Union[list[str], None]
  prompt: str
  
  def __init__(self, articleURL: str, correct_answer: str, prompt: str, answer_options: list[str]=None,question: str=None, correct_answer_id = None):
    self.articleURL = articleURL
    self.question = question
    self.correct_answer = correct_answer
    self.correct_answer_id = correct_answer_id
    self.answer_options = answer_options
    self.prompt = prompt

  def get_highest_question_id(self):
      highest_question = question_collection.find_one(sort=[("questionId", -1)])
      if highest_question:
          return highest_question["questionId"]
      else:
          return 0

  def save(self):
    question_collection.insert_one({
                    "article": self.articleURL,
                    "question": self.question,
                    "answers": self.answers,
                    "correct_answer": self.correct_answer_id,
                    "questionId": self.get_highest_question_id() + 1,
                    })