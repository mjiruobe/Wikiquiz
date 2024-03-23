from controller.wikidata import WikiDataInterface
class WikiNode:
    type: str
    value: str
    id: str

    def __init__(self, type, value, id):
        self.type = type
        self.value = value
        self.id = id

    @staticmethod
    def fromWikipedia(wikiURL):
        mainNode_Id = WikiDataInterface.get_wikidata_id_from_wikipedia_url(wikiURL)
        mainNode_value = WikiDataInterface.get_name_of_entity(mainNode_Id)
        mainNode_type = WikiDataInterface.get_name_of_entity(WikiDataInterface.get_id_of_instanceof(mainNode_Id))
        return WikiNode(mainNode_type, mainNode_value, mainNode_Id)
    
    @staticmethod
    def fromEntityProperty(entity, property_id):
        property_object_id = WikiDataInterface.get_property_of_entity(entity.id, property_id)
        node_type = WikiDataInterface.get_name_of_entity(WikiDataInterface.get_id_of_instanceof(property_object_id))
        node_value = WikiDataInterface.get_name_of_entity(property_object_id)
        return WikiNode(node_type, node_value, property_object_id)