from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel , UserModel , UserLoginModel
from .service import UserService , verify_password
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token , decode_token
from datetime import timedelta     
from fastapi.responses import JSONResponse


auth_router = APIRouter()

user_service = UserService()

REFRESH_TOKEN_EXPIRY = timedelta(days=2)

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

     if user is not None:
          if verify_password(password, user.password_hash):
               access_token = create_access_token(user_data={"uid": str(user.uid), "email": user.email})
               

               refresh_token = create_access_token(user_data={"uid": str(user.uid), "email": user.email}, refresh=True , expiry=REFRESH_TOKEN_EXPIRY)
               
               return JSONResponse(content={
                    "message":"login successfull",
                    "user":{
                         "uid": str(user.uid),
                         "email": user.email,
                         "username": user.username
                    },
                    "access_token": access_token,
                      "refresh_token": refresh_token}, 
                      status_code=status.HTTP_200_OK)
          
          else:
               raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
               )
     raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid credentials"
     )
               
