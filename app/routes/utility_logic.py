from utility_logics.mathematical.prime import generate_prime_numbers
from utility_logics.mathematical.factorial import calculate_factorial
from fastapi import APIRouter, Depends, HTTPException
from models.utilities import PrimeResponse, FactorialResponse
from models.user import User
from routes.user import get_current_user
from utility_logics.logging import log_utility_usage  # Import the logging function

router4 = APIRouter()

@router4.post("/generate_prime_numbers", response_model=PrimeResponse, tags=["Mathematical Utilities"])
async def generate_primes(limit: int, current_user: User = Depends(get_current_user)):
    """
    Generates prime numbers up to a given limit.
    Logs the usage of this utility in the database.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    primes = generate_prime_numbers(limit)  # Use the imported function
    
    # Log utility usage
    log_utility_usage(user_id=current_user.id, utility_name="generate_prime_numbers", parameters={"limit": limit})
    
    return PrimeResponse(primes=primes)


@router4.post("/calculate_factorial", response_model=FactorialResponse, tags=["Mathematical Utilities"])
async def calculate_factorial_route(number: int, current_user: User = Depends(get_current_user)):
    """
    Calculates the factorial of a given number.
    Logs the usage of this utility in the database.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    try:
        result = calculate_factorial(number)
        
        # Log utility usage
        log_utility_usage(user_id=current_user.id, utility_name="calculate_factorial", parameters={"number": number})
        
        return FactorialResponse(factorial=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
