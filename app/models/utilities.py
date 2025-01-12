from typing import Optional, List

from pydantic import BaseModel

class PythonUtilities(BaseModel):
    name: str
    description: str
    url: str
    category: str

    class Config:
        orm_mode = True

class PrimeResponse(BaseModel):
    primes: List[int]


class FactorialResponse(BaseModel):
    factorial: int

class FibonacciResponse(BaseModel):
    fibonacci_sequence: List[int]

class ScrambleResponse(BaseModel):
    scrambled_text: str

from pydantic import BaseModel

