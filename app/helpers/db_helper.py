from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_session():
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
