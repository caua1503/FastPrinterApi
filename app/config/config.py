from dotenv import load_dotenv
import os
caminho = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(caminho, ".env"))

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
DATABASE_URL = os.getenv("DATABASE_URL")