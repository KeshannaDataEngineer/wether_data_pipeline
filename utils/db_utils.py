import os
import sqlalchemy

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")  
    engine = sqlalchemy.create_engine(db_url)
    connection = engine.connect()
    return connection

def close_db_connection(connection):
    connection.close()
