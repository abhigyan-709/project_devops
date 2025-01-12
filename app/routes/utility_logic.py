from utility_logics.mathematical.prime import generate_prime_numbers
from fastapi import APIRouter, Depends, HTTPException
from models.utilities import PrimeResponse, FactorialResponse, FibonacciResponse, DownloadRequest, DownloadResponse
from utility_logics.mathematical.prime import generate_prime_numbers 
from utility_logics.mathematical.factorial import calculate_factorial
from utility_logics.mathematical.fibonacci import fibonacci_sequence # Import the function
from utility_logics.text_strings.scramble import scrambled_text
from utility_logics.downloaders.igvideo import download_instagram_video
from models.user import User
from routes.user import get_current_user
from pymongo import MongoClient

route4 = APIRouter()

@route4.post("/generate_prime_numbers", response_model=PrimeResponse, tags=["Mathematical Utilities"])
async def generate_primes(limit: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    primes = generate_prime_numbers(limit)  # Use the imported function
    return PrimeResponse(primes=primes)


@route4.post("/calculate_factorial", response_model=FactorialResponse, tags=["Mathematical Utilities"])
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
    
@route4.post("/generate_fibonacci_sequence", response_model=FibonacciResponse, tags=["Mathematical Utilities"])
async def generate_fibonacci_sequence(limit: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    try:
        sequence = fibonacci_sequence(limit)  # Use the imported function
        return FibonacciResponse(fibonacci_sequence=sequence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
@route4.post("/scramble_text", tags=["Text Utilities"])
async def scramble_text_route(text: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    try:
        result = scrambled_text(text)
        return {"scrambled_text": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
@route4.post("/download_video", response_model=DownloadResponse, tags=["Video Downloaders"])
async def download_video(request: DownloadRequest):
    try:
        message = download_instagram_video(request.url, request.filename)
        return DownloadResponse(message=message, filename=request.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

