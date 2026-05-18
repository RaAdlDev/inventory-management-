from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import settings

engine = create_engine(settings.database_url)
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = LocalSession()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()