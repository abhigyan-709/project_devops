from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from database.db import db
from models.user import User
from models.token import Token
from typing import Union
from pymongo import MongoClient
import secrets
from bson import ObjectId
from fastapi.responses import JSONResponse

route2 = APIRouter()
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create an instance of CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": data["username"]})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Fetch user details including the role from the database
        db_client = db.get_client()  # Use db.get_client directly
        user_from_db = db_client[db.db_name]["user"].find_one({"username": username})
        if user_from_db is None:
            raise credentials_exception

        user = User(**user_from_db)  # Convert database response to User model
        return user
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

@route2.get("/")
async def root():
    # Test MongoDB connection
    client = db.get_client()
    return {"message": "Connected to MongoDB successfully!"}

@route2.post("/token", response_model=Token, tags=["Login & Authentication"])
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db_client: MongoClient = Depends(db.get_client)
):
    user_from_db = db_client[db.db_name]["user"].find_one({"username": form_data.username})
    
    if user_from_db and verify_password(form_data.password, user_from_db['password']):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"username": form_data.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@route2.post("/register/", tags=["User Registration"])
async def register(user: User, db_client: MongoClient = Depends(db.get_client)):
    # Check if the username is already taken
    existing_user_username = db_client[db.db_name]["user"].find_one({"username": user.username})
    if existing_user_username:
        raise HTTPException(status_code=400, detail="Username is already taken")

    # Check if the email is already taken
    existing_user_email = db_client[db.db_name]["user"].find_one({"email": user.email})
    if existing_user_email:
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Hash the password before storing it in the database
    user_dict = user.dict()
    user_dict['password'] = get_password_hash(user.password)
    
    # Insert the user into the database
    result = db_client[db.db_name]["user"].insert_one(user_dict)
    
    # Convert ObjectId to string
    user_dict["_id"] = str(result.inserted_id)

    # Return response with the user data
    return JSONResponse(content=user_dict, status_code=201)


@route2.get("/users/me", response_model=User, tags=["Read User & Current User"])
async def read_current_user(current_user: User = Depends(get_current_user), db_client: MongoClient = Depends(db.get_client)):
    # Use the username from the current_user object to filter the database query
    user_from_db = db_client[db.db_name]["user"].find_one({"username": current_user.username})

    if user_from_db:
        return user_from_db

    raise HTTPException(status_code=404, detail="User not found")



@route2.get("/users/{user_id}", response_model=User, tags=["Read User & Current User"])
async def read_user_by_id(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db_client: MongoClient = Depends(db.get_client)
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own user details")

    user_from_db = db_client[db.db_name]["user"].find_one({"_id": ObjectId(user_id)})
    
    if user_from_db:
        return user_from_db

    raise HTTPException(status_code=404, detail="User not found")
