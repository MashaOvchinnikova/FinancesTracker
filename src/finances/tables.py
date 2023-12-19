from sqlalchemy import Column, Integer, ForeignKey, String, Date, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    message = Column(String)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    password_hash = Column(Text)


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    kind = Column(String)
    amount = Column(Numeric(10, 2))
    description = Column(String, nullable=True)



