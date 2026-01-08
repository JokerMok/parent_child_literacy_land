from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.db.session import get_db
from app.models.scene import Scene
from app.models.card import Card
from app.core.schemas import SceneCreate, SceneResponse, CardResponse

router = APIRouter()

# 获取场景列表
@router.get("/", response_model=List[SceneResponse])
async def get_scenes(
    db: Session = Depends(get_db),
    status: Optional[int] = Query(None, description="按状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    query = db.query(Scene)
    
    if status is not None:
        query = query.filter(Scene.status == status)
    
    scenes = query.order_by(desc(Scene.created_at))\
                .offset((page - 1) * page_size)\
                .limit(page_size)\
                .all()
    
    return scenes

# 获取场景详情
@router.get("/{scene_id}", response_model=SceneResponse)
async def get_scene(
    scene_id: int,
    db: Session = Depends(get_db)
):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    return scene

# 创建场景
@router.post("/", response_model=SceneResponse)
async def create_scene(
    scene: SceneCreate,
    db: Session = Depends(get_db)
):
    db_scene = Scene(**scene.dict())
    db.add(db_scene)
    db.commit()
    db.refresh(db_scene)
    
    return db_scene

# 更新场景
@router.put("/{scene_id}", response_model=SceneResponse)
async def update_scene(
    scene_id: int,
    scene: SceneCreate,
    db: Session = Depends(get_db)
):
    db_scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not db_scene:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    for key, value in scene.dict().items():
        setattr(db_scene, key, value)
    
    db.commit()
    db.refresh(db_scene)
    
    return db_scene

# 删除场景
@router.delete("/{scene_id}")
async def delete_scene(
    scene_id: int,
    db: Session = Depends(get_db)
):
    db_scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not db_scene:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    db.delete(db_scene)
    db.commit()
    
    return {"message": "场景删除成功"}

# 获取场景下的卡片
@router.get("/{scene_id}/cards", response_model=List[CardResponse])
async def get_scene_cards(
    scene_id: int,
    db: Session = Depends(get_db),
    status: Optional[int] = Query(None, description="按状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    # 先检查场景是否存在
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="场景不存在")
    
    query = db.query(Card).filter(Card.scene_id == scene_id)
    
    if status is not None:
        query = query.filter(Card.status == status)
    
    cards = query.order_by(desc(Card.created_at))\
                .offset((page - 1) * page_size)\
                .limit(page_size)\
                .all()
    
    return cards
