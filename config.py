from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.Product import Base

#sqlite just to keep it simple since it doesn't need installation or servers
engine = create_engine("sqlite:///./sqlitedatabase.db")

# Creates all tables defined by Base subclasses (e.g. Product) if they don't exist yet
# IF MODEL CHANGES, CREATE ALL WON'T UPDATE THE TABLE AUTOMATICALLY, a migration needs to be created.
Base.metadata.create_all(bind=engine)

# Every time we connect to something (server, db etc..) we create a new session
# db.commit() - commits the transaction to the database when autocommit is False
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency that opens and closes a session per request
def get_db():
    db = SessionLocal()
    try:
        # if this was return, then the session would be closed after the function ends
        # yield servers the db and then wait
        # under the hood FASTAPI is resuming this function after it's done with the api call. That closes the session by running finally
        yield db 
    finally:
        db.close()