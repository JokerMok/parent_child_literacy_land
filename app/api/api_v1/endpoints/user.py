from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.user import User

router = APIRouter()

# 登录接口
@router.post("/login")
async def login(
    uid: int,
    openid: str,
    nickname: Optional[str] = None,
    avatarUrl: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """用户登录"""
    try:
        # 查找现有用户
        user = db.query(User).filter(User.id == uid).first()
        
        if user:
            # 更新用户信息
            if openid:
                user.openid = openid
            if nickname:
                user.nickname = nickname
            if avatarUrl:
                user.avatar_url = avatarUrl
        else:
            # 创建新用户
            user = User(
                id=uid,
                openid=openid,
                nickname=nickname,
                avatar_url=avatarUrl,
                username=f"user_{uid}"
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)
        
        return {
            "code": 200,
            "message": "登录成功",
            "data": {
                "uid": user.id,
                "nickname": user.nickname,
                "avatarUrl": user.avatar_url,
                "openid": user.openid
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

# 获取用户信息
@router.get("/user/{uid}")
async def get_user_info(
    uid: int,
    db: Session = Depends(get_db)
):
    """获取用户信息"""
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "uid": user.id,
            "nickname": user.nickname,
            "avatarUrl": user.avatar_url,
            "openid": user.openid,
            "created_at": user.created_at
        }
    }

# 更新用户信息
@router.post("/user/update")
async def update_user_info(
    uid: int,
    nickname: Optional[str] = None,
    avatarUrl: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if nickname:
        user.nickname = nickname
    if avatarUrl:
        user.avatar_url = avatarUrl
    
    db.commit()
    db.refresh(user)
    
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "uid": user.id,
            "nickname": user.nickname,
            "avatarUrl": user.avatar_url
        }
    }

# 分析图片获取热区
@router.post("/analyze")
async def analyze_image(
    file_url: str,
    db: Session = Depends(get_db)
):
    """分析图片获取热区"""
    try:
        # 模拟分析结果
        mock_result = {
            "code": 200,
            "message": "分析成功",
            "data": [
                {
                    "text": "示例文字1",
                    "rect": [0.2, 0.2, 0.3, 0.15]
                },
                {
                    "text": "示例文字2",
                    "rect": [0.5, 0.5, 0.25, 0.12]
                }
            ]
        }
        
        return mock_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

# 用户创建卡片
@router.post("/user/create_card")
async def create_user_card(
    uid: int,
    scene_title: str,
    image_url: str,
    hotspots: list,
    db: Session = Depends(get_db)
):
    """用户创建卡片"""
    try:
        from app.models.card import Card
        from app.models.hotspot import Hotspot
        import time
        import json
        
        # 创建卡片
        new_card = Card(
            scene_id=1,  # 默认场景ID
            card_key=f"user_{uid}_{int(time.time())}",
            image_url=image_url,
            name=scene_title,
            status=1  # 直接通过审核
        )
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        
        # 保存热区数据
        for hotspot_item in hotspots:
            rect_json = json.dumps(hotspot_item.get("rect", []))
            db_hotspot = Hotspot(
                card_id=new_card.id,
                text=hotspot_item.get("text", ""),
                pinyin=hotspot_item.get("pinyin", ""),
                audio_url=hotspot_item.get("audio_url", ""),
                rect_json=rect_json
            )
            db.add(db_hotspot)
        
        db.commit()
        
        return {
            "code": 200,
            "message": "卡片创建成功",
            "data": {
                "card_id": new_card.id,
                "card_key": new_card.card_key,
                "image_url": new_card.image_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建卡片失败: {str(e)}")
