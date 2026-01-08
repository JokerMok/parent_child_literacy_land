from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Hotspot 相关模型
class HotspotItem(BaseModel):
    text: str = Field(..., description="热点文字")
    pinyin: Optional[str] = Field("", description="拼音")
    audio_url: Optional[str] = Field("", description="音频URL")
    rect: List[float] = Field(..., description="热点矩形坐标 [left, top, width, height]")

class HotspotResponse(HotspotItem):
    id: int = Field(..., description="热点ID")
    card_id: int = Field(..., description="所属卡片ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

# Card 相关模型
class CardBase(BaseModel):
    scene_id: int = Field(..., description="所属场景ID")
    image_url: str = Field(..., description="卡片图片URL")
    name: str = Field(..., description="卡片名称")
    status: Optional[int] = Field(0, description="状态: 0-待审核, 1-已通过, 2-已拒绝")

class CardCreate(CardBase):
    pass

class CardResponse(CardBase):
    id: int = Field(..., description="卡片ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    hotspots: Optional[List[HotspotResponse]] = Field([], description="卡片热点列表")

    class Config:
        from_attributes = True

# Scene 相关模型
class SceneBase(BaseModel):
    title: str = Field(..., description="场景标题")
    description: Optional[str] = Field("", description="场景描述")
    cover_url: Optional[str] = Field("", description="场景封面URL")
    status: Optional[int] = Field(1, description="状态: 0-禁用, 1-启用")

class SceneCreate(SceneBase):
    pass

class SceneResponse(SceneBase):
    id: int = Field(..., description="场景ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

# 热区创建和更新模型
class HotspotCreate(BaseModel):
    card_id: int = Field(..., description="所属卡片ID")
    text: str = Field(..., description="热点文字")
    pinyin: Optional[str] = Field("", description="拼音")
    audio_url: Optional[str] = Field("", description="音频URL")
    rect: List[float] = Field(..., description="热点矩形坐标 [left, top, width, height]")

class HotspotUpdate(BaseModel):
    text: Optional[str] = Field(None, description="热点文字")
    pinyin: Optional[str] = Field(None, description="拼音")
    audio_url: Optional[str] = Field(None, description="音频URL")
    rect: Optional[List[float]] = Field(None, description="热点矩形坐标 [left, top, width, height]")

# 保存热区请求模型
class SaveHotspotsRequest(BaseModel):
    card_id: int = Field(..., description="卡片ID")
    hotspots: List[HotspotCreate] = Field(..., description="热区列表")
