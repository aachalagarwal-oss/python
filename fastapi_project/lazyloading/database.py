from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.engine import Engine



SQLALCHEMY_DATABASE_URL='sqlite:///./lazy_eager.db'

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}, echo=True)


SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base=declarative_base()



@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


event.listen(engine, "connect", enable_sqlite_foreign_keys)
