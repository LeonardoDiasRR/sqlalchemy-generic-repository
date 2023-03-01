from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Index
from sqlalchemy.orm import sessionmaker

# DATABASE CONNECTION CONFGIG
db_url = f'sqlite:///database.db'

engine = create_engine(db_url, echo=False, pool_size=5)
Session = sessionmaker(bind=engine)
