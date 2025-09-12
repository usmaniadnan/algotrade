from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = os.path.join(BASE_DIR, '.env')

try:
    with open(dotenv_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value.strip('"'))
except FileNotFoundError:
    print(f"Warning: .env file not found at {dotenv_path}")


DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
