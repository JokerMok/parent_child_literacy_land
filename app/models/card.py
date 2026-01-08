from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Card(Base):
    __tablename__ = "t_cards"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="卡片ID")
    scene_id = Column(Integer, ForeignKey("t_scenes.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属场景ID")
    card_key = Column(String(100), nullable=True, unique=True, index=True, comment="卡片唯一标识")
    image_url = Column(String(255), nullable=False, comment="卡片图片URL")
    name = Column(String(50), nullable=False, default="", comment="卡片名称")
    status = Column(Integer, nullable=False, default=1, index=True, comment="状态: 0-待审核, 1-已通过, 2-已拒绝")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    hotspots = relationship("Hotspot", backref="card", cascade="all, delete-orphan")
