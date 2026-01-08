from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "t_users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="用户ID")
    openid = Column(String(100), unique=True, nullable=False, index=True, comment="微信OpenID")
    nickname = Column(String(50), nullable=False, default="", comment="用户昵称")
    avatar = Column(String(255), nullable=False, default="", comment="用户头像URL")
    is_vip = Column(Integer, nullable=False, default=0, index=True, comment="是否VIP: 0-普通用户, 1-VIP用户")
    vip_expire_time = Column(DateTime, nullable=True, index=True, comment="VIP到期时间")
    voice_id = Column(String(100), nullable=False, default="", comment="克隆音色ID")
    daily_upload_count = Column(Integer, nullable=False, default=0, comment="今日上传图片数量")
    last_upload_date = Column(Date, nullable=True, comment="最后上传日期")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间")
