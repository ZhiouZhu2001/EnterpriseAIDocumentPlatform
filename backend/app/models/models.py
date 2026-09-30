from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, CheckConstraint
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="user")
    ticket_reviews: Mapped[list["TICKET_REVIEW"]] = relationship("TICKET_REVIEW", back_populates="reviewer")
    documents: Mapped[list["DOCUMENT"]] = relationship("DOCUMENT", back_populates="user")
class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="tickets")
    ticket_reviews: Mapped[list["TICKET_REVIEW"]] = relationship("TICKET_REVIEW", back_populates="ticket")

class VISITOR_SPACE(Base):
    __tablename__ = "visitor_space"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    documents: Mapped[list["DOCUMENT"]] = relationship("DOCUMENT", back_populates="visitor_space")

class DOCUMENT(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL) <> (visitor_space_id IS NOT NULL)",
            name="ck_documents_exactly_one_owner",
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visitor_space_id: Mapped[int| None]  = mapped_column(Integer, ForeignKey("visitor_space.id"), nullable=True)
    user_id: Mapped[int| None]  = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expired_at: Mapped[datetime| None]  = mapped_column(DateTime, nullable=True)
    user: Mapped[User | None] = relationship("User", back_populates="documents")
    visitor_space: Mapped[VISITOR_SPACE | None] = relationship("VISITOR_SPACE", back_populates="documents")

class TICKET_REVIEW(Base):
    __tablename__ = "ticket_reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("tickets.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reviewer: Mapped[User] = relationship("User", back_populates="ticket_reviews")
    ticket: Mapped[Ticket] = relationship("Ticket", back_populates="ticket_reviews")
