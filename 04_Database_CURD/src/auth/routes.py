from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel , UserModel , UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token , decode_token

auth_router = APIRouter()

user_service = UserService()

@auth_router.post("/signup" , status_code=status.HTTP_201_CREATED ,response_model=UserModel)
async def create_user_account(user_data : UserCreateModel ,
                              session : AsyncSession = Depends(get_session)):
     
     email = user_data.email
     
     user_exists = await user_service.user_exists(email=email , session=session)

     if user_exists:
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="User with this email already exists"
          )
     
     return await user_service.create_user(user_data=user_data, session=session)

@auth_router.post("/login")
async def login_user(user_login_data : UserLoginModel,
                     session : AsyncSession = Depends(get_session)):
     
     email = user_login_data.email
     password = user_login_data.password
     
     user = await user_service.get_user_by_email(email=user_login_data.email, session=session)

     if not user:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User with this email does not exist"
          )

     if not verify_password(password, user.password_hash):
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="Invalid password"
          )

     access_token = create_access_token(user_data={
          "uid" : user.uid,
          "email" : user.email,
          "username" : user.username
     })

     return {
          "access_token" : access_token,
          "token_type" : "bearer"
     }


