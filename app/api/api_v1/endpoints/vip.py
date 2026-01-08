from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.user import User
from app.models.order import Order

router = APIRouter()

# 获取用户VIP状态
@router.get("/status")
async def get_vip_status(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户VIP状态"""
    try:
        # 查询用户
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 查询最新的有效订单
        active_order = db.query(Order)\
            .filter(Order.user_id == user_id, Order.status == 1)\
            .order_by(Order.created_at.desc())\
            .first()
        
        is_vip = False
        expire_time = None
        
        if active_order and active_order.expire_time and active_order.expire_time > datetime.now():
            is_vip = True
            expire_time = active_order.expire_time
        
        return {
            "user_id": user_id,
            "is_vip": is_vip,
            "expire_time": expire_time,
            "created_at": user.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取VIP状态失败: {str(e)}")

# 开通VIP
@router.post("/activate")
async def activate_vip(
    user_id: int,
    duration: int,  # 时长，单位：月
    db: Session = Depends(get_db)
):
    """开通VIP会员"""
    try:
        # 查询用户
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 计算过期时间
        now = datetime.now()
        expire_time = now + timedelta(days=duration * 30)
        
        # 创建订单
        new_order = Order(
            user_id=user_id,
            order_type="vip",
            amount=9.9 * duration,  # 假设每月9.9元
            status=1,
            duration=duration,
            expire_time=expire_time
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        return {
            "order_id": new_order.id,
            "user_id": user_id,
            "amount": new_order.amount,
            "duration": duration,
            "expire_time": expire_time,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"开通VIP失败: {str(e)}")

# 获取VIP价格列表
@router.get("/prices")
async def get_vip_prices(
    db: Session = Depends(get_db)
):
    """获取VIP价格列表"""
    try:
        # 这里可以从数据库或配置中获取价格列表
        prices = [
            {"duration": 1, "price": 9.9, "description": "月度会员"},
            {"duration": 3, "price": 26.9, "description": "季度会员"},
            {"duration": 12, "price": 99.9, "description": "年度会员"}
        ]
        
        return {"prices": prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取VIP价格失败: {str(e)}")

# 获取用户订单列表
@router.get("/orders")
async def get_user_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户订单列表"""
    try:
        # 查询用户订单
        orders = db.query(Order)\
            .filter(Order.user_id == user_id)\
            .order_by(Order.created_at.desc())\
            .all()
        
        return {
            "user_id": user_id,
            "orders": [{"id": order.id, "amount": order.amount, "duration": order.duration, "status": order.status, "created_at": order.created_at, "expire_time": order.expire_time} for order in orders]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取订单列表失败: {str(e)}")
