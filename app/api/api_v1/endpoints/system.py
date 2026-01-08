from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

# 获取系统配置
@router.get("/config")
async def get_system_config(
    db: Session = Depends(get_db)
):
    """获取系统配置"""
    # 模拟系统配置数据
    # 在实际项目中，这些配置可能来自数据库或配置文件
    config = {
        "version_number": settings.PROJECT_VERSION,
        "enable_upload": True,
        "max_upload_size": settings.MAX_FILE_SIZE,
        "enable_ai_analysis": True,
        "version_info": "亲子识字乐园 v1.0.0，支持场景识字、自定义卡片等功能",
        "user_agreement": "用户协议：使用本服务即表示您同意遵守相关条款..."
    }
    
    return config
