from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600

token_blocklist = aioredis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True
) 

async def add_jti_to_blocklist(jti : str) -> None:
    await token_blocklist.set(
        name = jti,
        value = 1,
        ex = JTI_EXPIRY
    ) # key and value set with expire 


async def token_in_blocklist(jti : str) -> bool:
    return await token_blocklist.exists(jti)