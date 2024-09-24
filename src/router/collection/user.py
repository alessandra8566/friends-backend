from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from schema.profile import UserProfileCreate
from schema.user import Token, TokenData, UserCreate, UserLogin
import conf, jwt, crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCollection(object):
    def __init__(self, db) -> None:
        self.db = db
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
    def create_user(self, user_info: UserCreate):
        hash_pwd = self.get_password_hash(user_info.password)
        user_info.password = hash_pwd
        db_user = crud.post_user(self.db, user_info)
        user_profile = UserProfileCreate(user_id=db_user.id, description="")
        crud.post_user_profile(self.db, user_profile)
        token_info = TokenData(
            user_id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            hashed_password=db_user.hashed_password,
            role=db_user.role
        )
        access_token = self.create_access_token(token_info)
        return Token(access_token=access_token)
    
    def login_user(self, user_info: UserLogin): 
        # Step 1: Fetch user from the database
        db_user = crud.get_user_by_email(self.db, user_info.email)
        # Step 2: Validate user existence and password
        if not db_user or not self.verify_password(user_info.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Step 3: Create JWT token
        access_token_expires = timedelta(minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
                data=TokenData(
                        user_id=db_user.id,
                        email=db_user.email,
                        name=db_user.name,
                        hashed_password=db_user.hashed_password,
                        role=db_user.role
                    ),
                expires_delta=access_token_expires
            )
        return Token(access_token=access_token)
    
    def create_access_token(self, data: TokenData, expires_delta: Optional[timedelta] = None):
        to_encode = data.model_dump().copy()
        to_encode.update({"user_id": str(data.user_id)})
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES) # 24 hours
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, conf.SECRET_KEY, algorithm=conf.ALGORITHM)
        return encoded_jwt
    
