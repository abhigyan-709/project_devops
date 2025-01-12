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
