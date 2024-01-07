from project import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, BigInteger, Text, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "sp_users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    full_name = Column(String(100), nullable=True)
    email = Column(String(50), nullable=True, unique=True)
    password = Column(Text, nullable=False)
    group = Column(String(20), nullable=True, default="user")
    register_ip = Column(String(30), nullable=True)
    register_timestamp = Column(BigInteger, nullable=False, default=func.unix_timestamp())

    def __init__(self, username, full_name, email, password, register_ip):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.password = password
        self.register_ip = register_ip


class Feature(Base):
    __tablename__ = "sp_features"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    icon = Column(Text, nullable=True)

    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = icon
