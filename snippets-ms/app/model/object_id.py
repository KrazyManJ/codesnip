from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_serializer


class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ])

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}
    

class ObjectIdBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, validation_alias="_id")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    @field_serializer('id')
    def serialize_object_id(self, value: Optional[PyObjectId], _info):
        if value is not None:
            return str(value)    
        return value
    
    def model_dump(self, **kwargs):
        kwargs.setdefault('by_alias', True)
        kwargs.setdefault('mode', "json")
        return super().model_dump(**kwargs)
    
    def to_mongo_document(self, **kwargs):
        parsed = self.model_dump()
        
        if 'id' in parsed:
            parsed['_id'] = ObjectId(parsed.pop('id'))
            
        return parsed