from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Order(Base):
    __tablename__ = "t_orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="订单ID")
    order_no = Column(String(50), unique=True, nullable=False, index=True, comment="订单号")
    user_id = Column(Integer, ForeignKey("t_users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    amount = Column(Numeric(10, 2), nullable=False, default=0.00, comment="订单金额")
    status = Column(Integer, nullable=False, default=0, index=True, comment="订单状态: 0-待支付, 1-已支付, 2-已取消")
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    pay_time = Column(DateTime, nullable=False, default="1970-01-01 00:00:00", comment="支付时间")
    
    # 关系
    user = relationship("User", backref="orders")
