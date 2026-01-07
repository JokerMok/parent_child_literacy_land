from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Hotspot(Base):
    __tablename__ = "t_hotspots"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="热点ID")
    card_id = Column(Integer, ForeignKey("t_cards.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属卡片ID")
    text = Column(String(100), nullable=False, default="", comment="热点文字")
    pinyin = Column(String(100), nullable=False, default="", comment="拼音")
    audio_url = Column(String(255), nullable=False, default="", comment="音频URL")
    rect_json = Column(Text, nullable=False, comment="热点矩形坐标JSON")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
