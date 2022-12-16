from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:       # used for pydantic model.
        orm_mode = True


class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase): #used to reference the expected attributes from the front end / URI
    id: int
    public: bool = True
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostResponse(PostBase): #sets the schema of the reposnse json to restrict information/fields inhereted fields from postbase
     id: int
     public: bool
     created_at: datetime
     owner_id: int
     owner: UserResponse

     class config:
         orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel): #used to reference the expected attributes from the front end / URI
    email: EmailStr
    password: str

class UserGetResponse(UserResponse):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) 