from neomodel import StructuredRel, StringProperty, DateTimeProperty, JSONProperty
from datetime import datetime


class GenericRelationship(StructuredRel):
    
    rel_type = StringProperty()

    
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    properties = JSONProperty()
