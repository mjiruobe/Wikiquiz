import requests
import sys
from wikidata.client import Client
import json
import random
import traceback
class WikiDataInterface:
    @staticmethod
    def get_entity_properties(entity_id):
        client = Client()
        entity = client.get(entity_id, load=True)
        label = entity.label

        properties = dict()
        for key, value in entity.data.items():
            properties[key] = value
        return properties

    @staticmethod
    def get_entity_data(entity_id):
        url = 'https://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': entity_id
        }
        response = requests.get(url, params=params)
        return response.json()['entities'][entity_id]

    @staticmethod
    def get_wikidata_id_from_wikipedia_url(wikipedia_url):
        # Extrahieren Sie den Seitentitel aus der URL
        title = wikipedia_url.split("/")[-1]

        url = 'https://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbgetentities',
            'sites': 'dewiki',
            'titles': title,
            'format': 'json',
            'props': ''
        }
        response = requests.get(url, params=params)
        entity_id = list(response.json()['entities'].keys())[0]
        return entity_id

    @staticmethod
    def get_property_of_entity(entity_id, property_id):
        try:
            if entity_id is None:
                return None
            return WikiDataInterface.get_entity_data(entity_id)['claims'][property_id][0]['mainsnak']['datavalue']['value']['id']
        except Exception as err:
            return None

    @staticmethod
    def get_id_of_instanceof(entity_id):
        try:
            if entity_id is None:
                return None
            return WikiDataInterface.get_entity_data(entity_id)['claims']['P31'][0]['mainsnak']['datavalue']['value']['id']
        except Exception as err:
            return None

    @staticmethod
    def get_name_of_entity(entity_id):
        try:
            if entity_id is None:
                return None
            return WikiDataInterface.get_entity_properties(entity_id)['labels']['de']['value']
        except Exception as err:
            return None
    
    @staticmethod
    def get_entity_properties(entity_id):
        client = Client()
        entity = client.get(entity_id, load=True)
        label = entity.label

        properties = dict()
        for key, value in entity.data.items():
            properties[key] = value
        return properties