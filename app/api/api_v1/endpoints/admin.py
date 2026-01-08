from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.db.session import get_db
from app.models.card import Card
from app.models.hotspot import Hotspot

router = APIRouter()

# 保存热区数据
@router.post("/save_hotspots")
async def save_hotspots(
    card_key: str,
    hotspots: list,
    db: Session = Depends(get_db)
):
    """保存卡片热区数据"""
    # 根据card_key查询卡片
    card = db.query(Card).filter(Card.card_key == card_key).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    # 删除该卡片的所有现有热区
    db.query(Hotspot).filter(Hotspot.card_id == card.id).delete()
    
    # 保存新的热区数据
    count = 0
    for item in hotspots:
        # 检查必要字段
        if "text" not in item or "rect" not in item:
            continue
        
        # 将rect列表转换为JSON字符串
        rect_json = json.dumps(item["rect"])
        
        # 创建新热区
        new_hotspot = Hotspot(
            card_id=card.id,
            text=item["text"],
            pinyin=item.get("pinyin", ""),
            audio_url=item.get("audio", ""),
            rect_json=rect_json
        )
        db.add(new_hotspot)
        count += 1
    
    db.commit()
    
    return {
        "code": 200,
        "message": f"成功保存 {count} 个热区",
        "count": count
    }
