import pytest
from app.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



SQLITE_URL = 'sqlite:///test.db'
engine = create_engine(SQLITE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope='function')
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()    
        Base.metadata.drop_all(bind=engine)