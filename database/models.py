from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    password = Column(String(255), nullable=False)

    reports = relationship('Report', back_populates='user')
    points_history = relationship('PointsHistory', back_populates='user')
    redeemed_rewards = relationship('RedeemedReward', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, points={self.points})>"

class Report(Base):
    __tablename__ = 'reports'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    street_name = Column(String(200), nullable=False)
    reported_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    photo_path = Column(String(255), nullable=True)
    points = Column(Integer, default=0, nullable=False)
    user = relationship('User', back_populates='reports')

    def __repr__(self):
        return f"<Report(id={self.id}, street_name={self.street_name}, reported_at={self.reported_at})>"


class PointsHistory(Base):
    __tablename__ = 'points_history'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    points_earned = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='points_history')

    def __repr__(self):
        return f"<PointsHistory(id={self.id}, points_earned={self.points_earned}, description={self.description})>"


class Reward(Base):
    __tablename__ = 'rewards'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = Column(String(100), nullable=False)
    points_required = Column(Integer, nullable=False)

    redeemed_rewards = relationship('RedeemedReward', back_populates='reward')

    def __repr__(self):
        return f"<Reward(id={self.id}, name={self.name}, points_required={self.points_required})>"


class RedeemedReward(Base):
    __tablename__ = 'redeemed_rewards'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    redeemed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    reward_id = Column(String(36), ForeignKey('rewards.id'), nullable=False)

    user = relationship('User', back_populates='redeemed_rewards')
    reward = relationship('Reward', back_populates='redeemed_rewards')

    def __repr__(self):
        return f"<RedeemedReward(id={self.id}, redeemed_at={self.redeemed_at}, user_id={self.user_id}, reward_id={self.reward_id})>"

# curent_dir = os.getcwd() 
# engine = create_engine(f'sqlite:///{curent_dir}/trashtagger.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# db_session = Session()


# users = db_session.query(User).all()

# for user in users:
#     print(user)
    