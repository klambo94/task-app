from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    email_verified = Column(DateTime(), nullable=True)
    image = Column(String, nullable=True)  # avatar URL from Google
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    boards = relationship("Board", back_populates="owner")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)                 # "oauth"
    provider = Column(String, nullable=False)             # "google"
    provider_account_id = Column(String, nullable=False)  # their Google ID
    refresh_token = Column(Text, nullable=True)
    access_token = Column(Text, nullable=True)
    expires_at = Column(Integer, nullable=True)
    token_type = Column(String, nullable=True)
    scope = Column(String, nullable=True)
    id_token = Column(Text, nullable=True)
    session_state = Column(String, nullable=True)

    user = relationship("User", back_populates="accounts")

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    session_token = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires = Column(DateTime(), nullable=False)

    user = relationship("User", back_populates="sessions")

class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    identifier = Column(String, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    expires = Column(DateTime(), nullable=False)