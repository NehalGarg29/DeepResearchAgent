from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.config import settings

Base = declarative_base()

class ResearchLog(Base):
    __tablename__ = "research_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    token_usage = Column(Integer, default=0)
    retrieval_count = Column(Integer, default=0)
    answer_status = Column(String, default="completed")
    evaluation_notes = Column(JSON, nullable=True)

class SessionManager:
    def __init__(self):
        self.engine = create_engine(settings.SQLITE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def log_research(self, query: str, token_usage: int, retrieval_count: int, status: str = "completed", evaluation: dict = None):
        session = self.Session()
        log_entry = ResearchLog(
            query_text=query,
            token_usage=token_usage,
            retrieval_count=retrieval_count,
            answer_status=status,
            evaluation_notes=evaluation
        )
        session.add(log_entry)
        session.commit()
        session.close()

session_manager = SessionManager()
