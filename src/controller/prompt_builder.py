import json
from controller.wikidata import WikiDataInterface
from model.question import Question
from model.wikinode import WikiNode

class PromptBuilder:
    def __init__(self, wikiURL):
        self._wikiURL = wikiURL
        self._entity_types = json.load(open("model/entity_types.json", "r"))
    
    def build(self):
        mainNode = WikiNode.fromWikipedia(self._wikiURL)
        relationships = self._entity_types[0]['relationships']
        questions = []
        for entity_attrs in relationships:
            property_id = entity_attrs['property_id']
            node = WikiNode.fromEntityProperty(mainNode, property_id)
            name = entity_attrs['name']
            llm_prompt = f"Frage nach den {name} von {mainNode.value} ({mainNode.type}). Stelle vier Optionen ({node.type}) bereit darunter die richtige Antwort {node.value}"
            questions.append(Question(self._wikiURL, node.value, llm_prompt))
        return questions
