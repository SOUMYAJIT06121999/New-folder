from fastapi import FastAPI, HTTPException
from models import Tea
from database import tea_collection
from bson import ObjectId

app = FastAPI()

# GET all teas
@app.get("/teas")
async def get_teas():
    teas = []
    async for tea in tea_collection.find():
        tea["_id"] = str(tea["_id"])
        teas.append(tea)
    return teas

# POST new tea
@app.post("/teas")
async def add_tea(tea: Tea):
    tea_dict = tea.dict(by_alias=True)
    result = await tea_collection.insert_one(tea_dict)
    tea_dict["_id"] = str(result.inserted_id)
    return tea_dict

# PUT (Update) tea
@app.put("/teas/{tea_id}")
async def update_tea(tea_id: str, updated_tea: Tea):
    result = await tea_collection.update_one(
        {"_id": ObjectId(tea_id)},
        {"$set": updated_tea.dict(exclude_unset=True, by_alias=True)},
    )
    if result.modified_count == 1:
        updated = await tea_collection.find_one({"_id": ObjectId(tea_id)})
        updated["_id"] = str(updated["_id"])
        return updated
    raise HTTPException(status_code=404, detail="Tea not found")

# DELETE tea
@app.delete("/teas/{tea_id}")
async def delete_tea(tea_id: str):
    result = await tea_collection.delete_one({"_id": ObjectId(tea_id)})
    if result.deleted_count == 1:
        return {"message": "Tea deleted successfully"}
    raise HTTPException(status_code=404, detail="Tea not found")
