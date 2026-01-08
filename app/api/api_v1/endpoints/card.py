from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import json
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
