from utility_logics.mathematical.prime import generate_prime_numbers
from fastapi import APIRouter, Depends, HTTPException
from models.utilities import PrimeResponse, FactorialResponse
from utility_logics.mathematical.prime import generate_prime_numbers 
from utility_logics.mathematical.factorial import calculate_factorial # Import the function
from database.db import get_db_client
from models.user import User
from routes.user import get_current_user
from pymongo import MongoClient

router4 = APIRouter()

@router4.post("/generate_prime_numbers", response_model=PrimeResponse, tags=["Mathematical Utilities"])
async def generate_primes(limit: int, current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(get_db_client)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    primes = generate_prime_numbers(limit)  # Use the imported function
    return PrimeResponse(primes=primes)


@router4.post("/calculate_factorial", response_model=FactorialResponse, tags=["Mathematical Utilities"])
async def calculate_factorial_route(number: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    try:
        result = calculate_factorial(number)
        return FactorialResponse(factorial=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))