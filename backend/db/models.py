from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime
from .database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    clarified_idea = Column(Text)
    execution_plan = Column(Text)
    risks = Column(Text)
    tools = Column(Text)
    market_analysis = Column(Text)
    created_at = Column(DateTime, default=datetime.now)