from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnector(ABC):  
    """
    Abstract base class for database connectors.
    It provides basic methods to create a SQLAlchemy engine and a session.
    """

    @abstractmethod
    def create_engine(self):
        pass  

    @abstractmethod
    def create_session(self):
        pass

class PostgresConnector(DatabaseConnector):
    """
    Concrete class for PostgreSQL database connector.
    """

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def create_engine(self):
        # DATABASE_URL = "postgresql://finance_db_user:1234@localhost:5432/finance_db"  # Or use environment variables
        url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return create_engine(url)

    def create_session(self):
        engine = self.create_engine()
        return sessionmaker(bind=engine)()
    

