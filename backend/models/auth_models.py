from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    emailVerified = Column(DateTime(), nullable=True)
    image = Column(String, nullable=True)
    createdAt = Column(DateTime(), server_default=func.now())
    updatedAt = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    organizations = relationship("OrganizationMember", back_populates="user")
    spaces = relationship("Space", back_populates="owner")
    reported_threads = relationship("Thread", foreign_keys="Thread.reporterId", back_populates="reporter")
    reviewing_threads = relationship("Thread", foreign_keys="Thread.reviewerId", back_populates="reviewer")
    assigned_threads = relationship("ThreadAssignee", back_populates="user")
    comments = relationship("Comment", back_populates="author")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True)
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)                 # "oauth"
    provider = Column(String, nullable=False)             # "google"
    providerAccountId = Column(String, nullable=False)  # their Google ID
    refreshToken = Column(Text, nullable=True)
    accessToken = Column(Text, nullable=True)
    expiresAt = Column(Integer, nullable=True)
    tokenType = Column(String, nullable=True)
    scope = Column(String, nullable=True)
    idToken = Column(Text, nullable=True)
    sessionState = Column(String, nullable=True)

    user = relationship("User", back_populates="accounts")

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    sessionToken = Column(String, unique=True, nullable=False, index=True)
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires = Column(DateTime(), nullable=False)

    user = relationship("User", back_populates="sessions")

class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    identifier = Column(String, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    expires = Column(DateTime(), nullable=False)