from typing import Optional

from pydantic import BaseModel

class PythonUtilities(BaseModel):
    name: str
    description: str
    url: str
    category: str

    class Config:
        orm_mode = True
