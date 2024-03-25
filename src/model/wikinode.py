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
        type_property = WikiDataInterface.get_id_of_instanceof(mainNode_Id)
        mainNode_type = WikiDataInterface.get_name_of_entity(type_property)
        return WikiNode(mainNode_type, mainNode_value, mainNode_Id)
    
    @staticmethod
    def fromEntityProperty(entity, property_id):
        property_object_id = WikiDataInterface.get_property_of_entity(entity.id, property_id)
        node_type = None
        node_value = None
        if not property_object_id is None:
            if "id" in property_object_id:
                type_property = WikiDataInterface.get_id_of_instanceof(property_object_id['id'])
                if WikiDataInterface.isMetaProperty(type_property):  # Its was already the type (meta property) so dont take the instance
                    type_property = property_object_id['id']
            else:
                type_property = property_id
            node_type = WikiDataInterface.get_name_of_entity(type_property)
            node_value = None if property_object_id is None else (WikiDataInterface.get_name_of_entity(property_object_id['id']) if "id" in property_object_id else (property_object_id['text'] if "text" in property_object_id else None))
        return WikiNode(node_type, node_value, property_object_id)