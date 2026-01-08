from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import json
import time
from typing import List, Optional

from app.db.session import get_db
from app.models.card import Card
from app.models.hotspot import Hotspot
from app.core.schemas import (
    CardCreate, CardResponse, HotspotItem, HotspotResponse,
    HotspotCreate, HotspotUpdate, SaveHotspotsRequest
)

router = APIRouter()

# 获取卡片列表
@router.get("/", response_model=List[CardResponse])
async def get_cards(
    db: Session = Depends(get_db),
    scene_id: Optional[int] = Query(None, description="按场景ID筛选"),
    status: Optional[int] = Query(None, description="按状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    query = db.query(Card)
    
    if scene_id:
        query = query.filter(Card.scene_id == scene_id)
    if status is not None:
        query = query.filter(Card.status == status)
    
    cards = query.order_by(desc(Card.created_at))\
                .offset((page - 1) * page_size)\
                .limit(page_size)\
                .all()
    
    return cards

# 获取卡片详情
@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    db: Session = Depends(get_db)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    return card

# 创建卡片
@router.post("/", response_model=CardResponse)
async def create_card(
    card: CardCreate,
    db: Session = Depends(get_db)
):
    db_card = Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    
    return db_card

# 更新卡片
@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card: CardCreate,
    db: Session = Depends(get_db)
):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    for key, value in card.dict().items():
        setattr(db_card, key, value)
    
    db.commit()
    db.refresh(db_card)
    
    return db_card

# 删除卡片
@router.delete("/{card_id}")
async def delete_card(
    card_id: int,
    db: Session = Depends(get_db)
):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    db.delete(db_card)
    db.commit()
    
    return {"message": "卡片删除成功"}

# 获取卡片热区
@router.get("/{card_id}/hotspots", response_model=List[HotspotResponse])
async def get_card_hotspots(
    card_id: int,
    db: Session = Depends(get_db)
):
    # 先检查卡片是否存在
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    # 查询卡片的所有热区
    hotspots = db.query(Hotspot).filter(Hotspot.card_id == card_id).all()
    
    # 将rect_json转换为rect列表
    for hotspot in hotspots:
        if hotspot.rect_json:
            hotspot.rect = json.loads(hotspot.rect_json)
    
    return hotspots

# 保存卡片热区
@router.post("/hotspots/save")
async def save_hotspots(
    request: SaveHotspotsRequest,
    db: Session = Depends(get_db)
):
    # 先检查卡片是否存在
    card = db.query(Card).filter(Card.id == request.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    # 删除该卡片的所有现有热区
    db.query(Hotspot).filter(Hotspot.card_id == request.card_id).delete()
    
    # 保存新的热区
    for hotspot_item in request.hotspots:
        # 将rect列表转换为JSON字符串
        rect_json = json.dumps(hotspot_item.rect)
        
        # 创建新热区
        db_hotspot = Hotspot(
            card_id=request.card_id,
            text=hotspot_item.text,
            pinyin=hotspot_item.pinyin,
            audio_url=hotspot_item.audio_url,
            rect_json=rect_json
        )
        db.add(db_hotspot)
    
    db.commit()
    
    return {"message": "热区保存成功", "count": len(request.hotspots)}

# 更新单个热区
@router.put("/hotspots/{hotspot_id}", response_model=HotspotResponse)
async def update_hotspot(
    hotspot_id: int,
    hotspot: HotspotUpdate,
    db: Session = Depends(get_db)
):
    db_hotspot = db.query(Hotspot).filter(Hotspot.id == hotspot_id).first()
    if not db_hotspot:
        raise HTTPException(status_code=404, detail="热区不存在")
    
    # 处理rect字段的转换
    update_data = hotspot.dict(exclude_unset=True)
    if "rect" in update_data:
        update_data["rect_json"] = json.dumps(update_data.pop("rect"))
    
    for key, value in update_data.items():
        setattr(db_hotspot, key, value)
    
    db.commit()
    db.refresh(db_hotspot)
    
    # 将rect_json转换为rect列表
    if db_hotspot.rect_json:
        db_hotspot.rect = json.loads(db_hotspot.rect_json)
    
    return db_hotspot

# 删除单个热区
@router.delete("/hotspots/{hotspot_id}")
async def delete_hotspot(
    hotspot_id: int,
    db: Session = Depends(get_db)
):
    db_hotspot = db.query(Hotspot).filter(Hotspot.id == hotspot_id).first()
    if not db_hotspot:
        raise HTTPException(status_code=404, detail="热区不存在")
    
    db.delete(db_hotspot)
    db.commit()
    
    return {"message": "热区删除成功"}

# 批量更新热区
@router.post("/hotspots/batch_update")
async def batch_update_hotspots(
    hotspots: List[HotspotUpdate],
    db: Session = Depends(get_db)
):
    updated_count = 0
    for hotspot in hotspots:
        db_hotspot = db.query(Hotspot).filter(Hotspot.id == hotspot.id).first()
        if db_hotspot:
            update_data = hotspot.dict(exclude_unset=True)
            if "rect" in update_data:
                update_data["rect_json"] = json.dumps(update_data.pop("rect"))
            
            for key, value in update_data.items():
                setattr(db_hotspot, key, value)
            updated_count += 1
    
    db.commit()
    
    return {"message": "批量更新成功", "updated_count": updated_count}

# 用户创建卡片
@router.post("/user/create_card")
async def create_user_card(
    uid: int,
    scene_title: str,
    image_url: str,
    hotspots: List[HotspotCreate],
    db: Session = Depends(get_db)
):
    """用户创建卡片"""
    try:
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
            rect_json = json.dumps(hotspot_item.rect)
            db_hotspot = Hotspot(
                card_id=new_card.id,
                text=hotspot_item.text,
                pinyin=hotspot_item.pinyin,
                audio_url=hotspot_item.audio_url,
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

# 更新卡片名称
@router.post("/update_name")
async def update_card_name(
    id: int,
    name: str,
    db: Session = Depends(get_db)
):
    """更新卡片名称"""
    card = db.query(Card).filter(Card.id == id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    card.name = name
    db.commit()
    db.refresh(card)
    
    return {
        "code": 200,
        "message": "名称更新成功"
    }

# 删除卡片（匹配小程序请求路径）
@router.post("/delete")
async def delete_card_by_post(
    id: int,
    db: Session = Depends(get_db)
):
    """删除卡片（POST请求，匹配小程序）"""
    card = db.query(Card).filter(Card.id == id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    db.delete(card)
    db.commit()
    
    return {
        "code": 200,
        "message": "卡片删除成功"
    }
