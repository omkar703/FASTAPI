from re import A
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Request , Depends
from src.auth.utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService
from typing import Any, List
from .auth.models import User


class TokenBearer(HTTPBearer):
    # when it get call then the init it check header and pass 403/401 
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    # here if the header is missing 
    async def __call__(self,  request : Request) -> HTTPAuthorizationCredentials | None:
        creds =  await super().__call__(request) 

        token = creds.credentials

        token_data  = decode_token(token)

      
        if not self.token_valid(token):
            raise HTTPException(status_code=401, detail={"error" : "Invalid token" ,
                                                         "resolution": "Please get new token"})
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=401, detail={"error" : "Token is in blocklist" , 
                                                         "resolution": "Please get new token"})
        
        self.verify_token_data(token_data)

        return token_data
    

    def token_valid(self , token : str) -> bool:
        token_data  = decode_token(token)

        # return true if the token data is not none else false 
        return token_data is not None

       
        
    def verify_token_data(self, token_data : dict) -> None:
        raise NotImplementedError("This method should be implemented in subclasses") 
    


        
        

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self , token_data : dict) -> None:
        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if token_data['refresh']:
            raise HTTPException(status_code=401, detail="Please provide access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data : dict) -> None:
        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if not token_data['refresh']:
            raise HTTPException(status_code=401, detail="Please provide refresh token")



async def get_current_user(token_details : dict = Depends(AccessTokenBearer()) ,
                     session: AsyncSession = Depends(get_session)):
    user_email = token_details["user"]["email"]

    user = await UserService().get_user_by_email(email=user_email , session=session)

    return user



class RoleChecker:
    def __init__(self, allowed_roles : List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, Current_User: User = Depends(get_current_user)) -> Any:
        if Current_User.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permited")