from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    content: Mapped[str] = mapped_column(Text)