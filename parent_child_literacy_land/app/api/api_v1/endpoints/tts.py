from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from app.db.session import get_db
from app.models.user import User
from app.services.tts_service import tts_service
from app.core.config import settings

router = APIRouter()

@router.post("/generate")
async def generate_tts(
    text: str = Query(..., description="要转换的文本"),
    voice_id: str = Query("", description="克隆的声音ID（可选）"),
    db: Session = Depends(get_db)
):
    """
    生成语音接口
    - VIP用户且有克隆音色时，使用克隆音
    - 普通用户使用Edge-TTS
    """
    try:
        # 生成唯一的输出文件名
        output_filename = f"tts_output_{uuid.uuid4()}.mp3"
        output_path = os.path.join(settings.UPLOAD_DIR, output_filename)
        
        # 调用TTS服务生成语音
        success = await tts_service.synthesize(text, voice_id, output_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="语音生成失败")
        
        # 返回音频文件URL（实际项目中应该返回完整的HTTP URL）
        return {
            "code": 0,
            "message": "语音生成成功",
            "data": {
                "audio_url": f"/{settings.UPLOAD_DIR}/{output_filename}",
                "voice_id": voice_id if voice_id else "system"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成语音失败: {str(e)}")
