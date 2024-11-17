from database.models import Base, User, Report, PointsHistory, Reward, RedeemedReward
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

print(Base)
# Maak de SQLite-engine
current_dir = os.getcwd()
print(current_dir)
engine = create_engine(f'sqlite:///{current_dir}\database/trashtagger.db')

# Maak alle tabellen in de database
Base.metadata.create_all(engine)

# Maak een sessie aan
Session = sessionmaker(bind=engine)
db_session = Session()

