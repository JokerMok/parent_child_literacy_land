from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Scene(Base):
    __tablename__ = "t_scenes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="场景ID")
    title = Column(String(100), nullable=False, default="", comment="场景标题")
    cover = Column(String(255), nullable=False, default="", comment="场景封面URL")
    description = Column(String(255), nullable=False, default="", comment="场景描述")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序字段")
    user_id = Column(Integer, ForeignKey("t_users.id", ondelete="CASCADE"), nullable=True, index=True, comment="创建者ID")
    is_public = Column(Integer, nullable=False, default=0, index=True, comment="是否公开: 0-私有, 1-公开")
    status = Column(Integer, nullable=False, default=1, index=True, comment="状态: 0-待审核, 1-已通过, 2-已拒绝")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    user = relationship("User", backref="scenes")
    cards = relationship("Card", backref="scene", cascade="all, delete-orphan")
