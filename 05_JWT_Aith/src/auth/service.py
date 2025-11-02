from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash , verify_password

class UserService:
    async def get_user_by_email(self , email : str , session : AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        return result.first()
    

    async def user_exists(self ,email , session : AsyncSession):
        user = await self.get_user_by_email(email=email, session=session)
        
        return True if user is not None else False
    
    async def create_user(self, user_data : UserCreateModel, session : AsyncSession):
        # convert the data into dict 
        user_data_dict = user_data.model_dump()
        user_data_dict['password_hash'] = generate_password_hash(user_data.password)

        user = User(**user_data_dict)
        session.add(user)
        await session.commit()
        return user
    
