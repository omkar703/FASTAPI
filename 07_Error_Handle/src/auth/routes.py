from hmac import new
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel , UserModel , UserLoginModel , UserBooksModel
from .service import UserService , verify_password
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token , decode_token
from datetime import timedelta  , datetime   
from fastapi.responses import JSONResponse
from src.dependencies import RefreshTokenBearer , AccessTokenBearer , get_current_user , RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.error import UserAlreadyExists

auth_router = APIRouter()

user_service = UserService()

RoleChecker = RoleChecker(["admin" , "user"])

REFRESH_TOKEN_EXPIRY = timedelta(days=2)

@auth_router.post("/signup" , status_code=status.HTTP_201_CREATED ,response_model=UserBooksModel)
async def create_user_account(user_data : UserCreateModel ,
                              session : AsyncSession = Depends(get_session)):
     
     email = user_data.email
     
     user_exists = await user_service.user_exists(email=email , session=session)

     if user_exists:
          UserAlreadyExists()
     
     return await user_service.create_user(user_data=user_data, session=session)

@auth_router.post("/login")
async def login_user(user_login_data : UserLoginModel,
                     session : AsyncSession = Depends(get_session)):
     
     email = user_login_data.email
     password = user_login_data.password
     
     user = await user_service.get_user_by_email(email=user_login_data.email, session=session)

     if user is not None:
          if verify_password(password, user.password_hash):
               access_token = create_access_token(user_data={"uid": str(user.uid), "email": user.email ,
                                                             "role" : user.role})
               

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
               

@auth_router.get('/refresh_token' , status_code=status.HTTP_200_OK )
async def get_new_access_token(token_details : dict = Depends(RefreshTokenBearer())): 
    
    '''
    {
  "token_details": {
    "user": {
      "uid": "0e5184d2-6b8c-4491-be43-caa37ba2e9ee",
      "email": "opdev@gmail.com"
    },
    "exp": 1762357177,
    "jti": "f7dbfab7-8be6-47da-ac84-0129e8f74fd5",
    "refresh": true
  }
}
'''

    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
         new_access_token = create_access_token(user_data=token_details['user'])
         return JSONResponse(content={"access_token": new_access_token}, status_code=status.HTTP_200_OK)

     # return JSONResponse(content={"message": "Token expired"}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"message": "Token expired"}, status_code=status.HTTP_401_UNAUTHORIZED)

@auth_router.get('/me' , response_model=UserBooksModel)
# here it go first in the get_current_user convert the token into usermodels and then pass it to the user 
async def get_user_details(user   : UserModel =  Depends(get_current_user) , _:bool = Depends(RoleChecker) ):
     return user



@auth_router.get('/logout')
async def revooke_token(token_details : dict = Depends(AccessTokenBearer())):
     print(token_details)
     jti = token_details['jti']

     await add_jti_to_blocklist(jti=jti)

     return JSONResponse(content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK)
