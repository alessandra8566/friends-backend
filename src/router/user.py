from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from router.collection.user import UserCollection
from schema.user import User
from . import validate_token, get_db
import schema, crud

router = APIRouter()

@router.get("", response_model=List[schema.User])
def read_users(limit: int = 10, db: Session = Depends(get_db), _: None = Depends(validate_token)):
    
    users = crud.get_users(db, limit=limit)
    return users

@router.get("/me", response_model=User)
async def read_user_me(db: Session = Depends(get_db), user: User = Depends(validate_token)):
    return user
    
@router.post("/sign-in", response_model=schema.Token)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    _collect = UserCollection(db)
    
    token = _collect.create_user(user)
    return token

@router.post("/login", response_model=schema.Token)
async def login_user(user: schema.UserLogin, db: Session = Depends(get_db)):
    _collect = UserCollection(db)
    
    token = _collect.login_user(user)
    return token
