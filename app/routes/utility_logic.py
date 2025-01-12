from utility_logics.mathematical.prime import generate_prime_numbers
from fastapi import APIRouter, Depends, HTTPException
from app.models.utilities import Utility, PrimeResponse
from app.utility_logics.mathematical.prime import generate_prime_numbers  # Import the function
from app.database.db import get_db_client
from app.models.user import User
from app.routes.user import get_current_user
from pymongo import MongoClient

router4 = APIRouter()

@router4.post("/generate_prime_numbers", response_model=PrimeResponse)
async def generate_primes(limit: int, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(get_db_client)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    primes = generate_prime_numbers(limit)  # Use the imported function
    return PrimeResponse(primes=primes)
