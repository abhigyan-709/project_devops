from fastapi import APIRouter, Depends, HTTPException
from database.db import db
from models.utilities import PythonUtilities
from models.user import User
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from routes.user import get_current_user


route3 = APIRouter()

@route3.post("/add_utilities", tags=["utilities"])
async def add_utilites(utility: PythonUtilities, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        db_client[db.db_name]["utilities"].insert_one(utility.model_dump())
        return JSONResponse(content={"message": "Utility added successfully"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
    
@route3.get("/get_utilities", tags=["utilities"])
async def get_utilities(current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        utilities = db_client[db.db_name]["utilities"].find()
        return JSONResponse(content={"message": "Utilities fetched successfully", "data": list(utilities)}, status_code=200)
    except:
        return JSONResponse(content={"message": "Error fetching utilities"}, status_code=500)
    
@route3.get("/get_utilities_by_category/{category}", tags=["utilities"])
async def get_utilities_by_category(category: str, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        utilities = db_client[db.db_name]["utilities"].find({"category": category})
        return JSONResponse(content={"message": "Utilities fetched successfully", "data": list(utilities)}, status_code=200)
    except:
        return JSONResponse(content={"message": "Error fetching utilities"}, status_code=500)
