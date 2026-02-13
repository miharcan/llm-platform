from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    request_id = Column(String)
    tenant_id = Column(String)
    country = Column(String)
    query = Column(String)
    latency_seconds = Column(Float)
    estimated_cost = Column(Float)
    num_sources = Column(Integer)
