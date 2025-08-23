from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class Tea(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    origin: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
