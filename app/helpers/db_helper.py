from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DATABASE_URL

def get_session():
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()