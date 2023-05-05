from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    """
    function to create a session to the database
    
    Returns:
        session: database session
    """
    # create a database engine
    engine = create_engine('sqlite:///real_estate.db')
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()
    # return the session
    return session
