from sqlalchemy import create_engine
from config import DATABASE_URL

#Criar uma engine async depois
async def get_engine(database_url:str = DATABASE_URL):
    print(database_url)
    return create_engine(database_url)