import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False