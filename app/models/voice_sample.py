from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class VoiceSample(Base):
    __tablename__ = "t_voice_samples"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="样本ID")
    user_id = Column(Integer, ForeignKey("t_users.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属用户ID")
    audio_url = Column(String(255), nullable=False, comment="原始录音URL")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    
    # 关系
    user = relationship("User", backref="voice_samples")
