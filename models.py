from pydantic import BaseModel, Field
from typing import Optional, Any
from bson import ObjectId
from pydantic_core import core_schema
from pydantic.json_schema import GetJsonSchemaHandler


# Custom ObjectId handler for Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler):
        schema = handler(core_schema.str_schema())
        schema.update(type="string")
        return schema


class Tea(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    origin: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True  # allow using `id` in responses but store `_id` in DB
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}  # serialize ObjectId as string
        schema_extra = {
            "example": {
                "name": "Green Tea",
                "origin": "China",
                "description": "A refreshing green tea.",
            }
        }   