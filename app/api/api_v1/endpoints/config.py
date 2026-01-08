from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.db.session import get_db
from app.models.card import Card
from app.models.hotspot import Hotspot

router = APIRouter()

# 获取卡片配置
@router.get("/{card_key}")
async def get_card_config(
    card_key: str,
    db: Session = Depends(get_db)
):
    """根据card_key获取卡片配置"""
    # 根据card_key查询卡片
    card = db.query(Card).filter(Card.card_key == card_key).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    # 查询卡片的所有热区
    hotspots = db.query(Hotspot).filter(Hotspot.card_id == card.id).all()
    
    # 构建响应数据
    result = []
    for hotspot in hotspots:
        if hotspot.rect_json:
            rect = json.loads(hotspot.rect_json)
            result.append({
                "text": hotspot.text,
                "pinyin": hotspot.pinyin,
                "audio": hotspot.audio_url,
                "rect": rect
            })
    
    return result
