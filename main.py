from fastapi import FastAPI, HTTPException, status
from models import Tea
from database import tea_collection
from bson import ObjectId
from bson.errors import InvalidId
from typing import List

app = FastAPI()

# Utility: Convert str -> ObjectId safely
def parse_object_id(tea_id: str) -> ObjectId:
    try:
        return ObjectId(tea_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid tea_id format")


# GET all teas
@app.get("/teas", response_model=List[Tea])
async def get_teas():
    teas = []
    async for tea in tea_collection.find():
        tea["_id"] = str(tea["_id"])
        teas.append(tea)
    return teas


# POST new tea
@app.post("/teas", status_code=status.HTTP_201_CREATED)
async def add_tea(tea: Tea):
    tea_dict = tea.dict(by_alias=True)
    result = await tea_collection.insert_one(tea_dict)
    tea_dict["_id"] = str(result.inserted_id)
    return tea_dict


# PUT (Update) tea
@app.put("/teas/{tea_id}")
async def update_tea(tea_id: str, updated_tea: Tea):
    obj_id = parse_object_id(tea_id)

    result = await tea_collection.update_one(
        {"_id": obj_id},
        {"$set": updated_tea.dict(exclude_unset=True, by_alias=True)},
    )

    if result.modified_count == 1:
        updated = await tea_collection.find_one({"_id": obj_id})
        updated["_id"] = str(updated["_id"])
        return updated

    raise HTTPException(status_code=404, detail="Tea not found")


# DELETE tea
@app.delete("/teas/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tea(tea_id: str):
    obj_id = parse_object_id(tea_id)

    result = await tea_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Tea deleted successfully"}

    raise HTTPException(status_code=404, detail="Tea not found")
