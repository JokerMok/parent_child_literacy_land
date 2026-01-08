from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, voice, tts, security, vip, scene, card, config, upload, admin, system, user

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
api_router.include_router(scene.router, prefix="/scenes", tags=["场景管理"])

# 卡片相关路由
api_router.include_router(card.router, prefix="/card", tags=["卡片管理"])

# 配置相关路由
api_router.include_router(config.router, prefix="/config", tags=["配置管理"])

# 上传相关路由
api_router.include_router(upload.router, prefix="/upload", tags=["上传管理"])

# 管理员相关路由
api_router.include_router(admin.router, prefix="/admin", tags=["管理员管理"])

# 系统相关路由
api_router.include_router(system.router, prefix="/system", tags=["系统管理"])

# 用户相关路由
api_router.include_router(user.router, prefix="", tags=["用户管理"])
