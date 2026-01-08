from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid

from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# 上传图片
@router.post("/")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传图片"""
    try:
        # 生成唯一文件名
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # 返回文件URL
        file_url = f"{settings.API_V1_STR}/upload/{filename}"
        
        return {
            "code": 200,
            "message": "上传成功",
            "data": {
                "file_url": file_url,
                "filename": filename
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

# 分析图片获取热区（模拟实现）
@router.post("/analyze")
async def analyze_image(
    file_url: str,
    db: Session = Depends(get_db)
):
    """分析图片获取热区"""
    try:
        # 模拟分析结果
        # 在实际项目中，这里应该调用AI模型进行图片分析
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

# 提供图片访问
@router.get("/{filename}")
async def get_image(
    filename: str,
    db: Session = Depends(get_db)
):
    """提供图片访问"""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="图片不存在")
        
        # 在实际项目中，这里应该返回图片文件
        # 由于FastAPI的FileResponse需要正确配置，这里简单返回文件URL
        return {
            "file_url": f"{settings.API_V1_STR}/upload/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取图片失败: {str(e)}")
