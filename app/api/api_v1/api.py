from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, voice, tts, security, vip, scene, card

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 声音克隆相关路由
api_router.include_router(voice.router, prefix="/voice", tags=["声音克隆"])

# TTS相关路由
api_router.include_router(tts.router, prefix="/tts", tags=["语音合成"])

# 内容安全相关路由
api_router.include_router(security.router, prefix="/security", tags=["内容安全"])

# VIP相关路由
api_router.include_router(vip.router, prefix="/vip", tags=["会员服务"])

# 场景相关路由
api_router.include_router(scene.router, prefix="/scene", tags=["场景管理"])

# 卡片相关路由
api_router.include_router(card.router, prefix="/card", tags=["卡片管理"])
