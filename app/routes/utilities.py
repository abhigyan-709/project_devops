import logging
from fastapi import APIRouter, Depends, HTTPException
from database.db import db
from models.utilities import PythonUtilities
from models.user import User
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from routes.user import get_current_user
from bson import ObjectId

route3 = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

@route3.post("/add_utilities", tags=["utilities"])
async def add_utilites(utility: PythonUtilities, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        db_client[db.db_name]["utilities"].insert_one(utility.model_dump())
        return JSONResponse(content={"message": "Utility added successfully"}, status_code=201)
    except Exception as e:
        logging.error(f"Error adding utility: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=500)

@route3.get("/get_utilities", tags=["utilities"])
async def get_utilities(current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        utilities = db_client[db.db_name]["utilities"].find()
        utilities_list = list(utilities)
        if not utilities_list:
            return JSONResponse(content={"message": "No utilities found"}, status_code=404)
        return JSONResponse(content={"message": "Utilities fetched successfully", "data": utilities_list}, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching utilities: {e}")
        return JSONResponse(content={"message": "Error fetching utilities", "error": str(e)}, status_code=500)

@route3.get("/get_utilities_by_category/{category}", tags=["utilities"])
async def get_utilities_by_category(category: str, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    
    try:
        utilities_cursor = db_client[db.db_name]["utilities"].find({"category": category})
        
        # Convert ObjectId to string in the result
        utilities_list = [
            {**utility, "_id": str(utility["_id"])} for utility in utilities_cursor
        ]
        
        if not utilities_list:
            return JSONResponse(content={"message": f"No utilities found for category {category}"}, status_code=404)
        
        return JSONResponse(content={"message": "Utilities fetched successfully", "data": utilities_list}, status_code=200)
    
    except Exception as e:
        logging.error(f"Error fetching utilities by category: {e}")
        return JSONResponse(content={"message": "Error fetching utilities by category", "error": str(e)}, status_code=500)

@route3.get("/get_utilities_by_name/{name}", tags=["utilities"])
async def get_utilities_by_name(name: str, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        utilities = db_client[db.db_name]["utilities"].find({"name": name})
        utilities_list = list(utilities)
        if not utilities_list:
            return JSONResponse(content={"message": f"No utilities found for name {name}"}, status_code=404)
        return JSONResponse(content={"message": "Utilities fetched successfully", "data": utilities_list}, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching utilities by name: {e}")
        return JSONResponse(content={"message": "Error fetching utilities by name", "error": str(e)}, status_code=500)

@route3.get("/get_utilities_by_name/{name}", tags=["utilities"])
async def get_utilities_by_name(name: str, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    
    try:
        utilities_cursor = db_client[db.db_name]["utilities"].find({"name": name})
        
        # Convert ObjectId to string in the result
        utilities_list = [
            {**utility, "_id": str(utility["_id"])} for utility in utilities_cursor
        ]
        
        if not utilities_list:
            return JSONResponse(content={"message": f"No utilities found for name {name}"}, status_code=404)
        
        return JSONResponse(content={"message": "Utilities fetched successfully", "data": utilities_list}, status_code=200)
    
    except Exception as e:
        logging.error(f"Error fetching utilities by name: {e}")
        return JSONResponse(content={"message": "Error fetching utilities by name", "error": str(e)}, status_code=500)


@route3.delete("/delete_utilities/{name}", tags=["utilities"])
async def delete_utilities(name: str, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    if current_user.role != "admin":
        return JSONResponse(content={"message": "You are not authorized to perform this action"}, status_code=401)
    try:
        result = db_client[db.db_name]["utilities"].delete_one({"name": name})
        if result.deleted_count == 0:
            return JSONResponse(content={"message": f"No utility found with name {name}"}, status_code=404)
        return JSONResponse(content={"message": "Utility deleted successfully"}, status_code=200)
    except Exception as e:
        logging.error(f"Error deleting utility: {e}")
        return JSONResponse(content={"message": "Error deleting utility", "error": str(e)}, status_code=500)
