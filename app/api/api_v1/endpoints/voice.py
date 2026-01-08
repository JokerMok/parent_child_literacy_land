from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.voice_sample import VoiceSample
from app.services.voice_service import voice_clone_service

router = APIRouter()

@router.post("/clone")
def clone_voice(
    user_id: int = 1,  # 实际项目中应该从JWT token中获取
    audio_file: UploadFile = File(..., description="上传的录音文件"),
    db: Session = Depends(get_db)
):
    """
    上传录音并克隆声音
    """
    try:
        # 1. 验证用户是否为VIP
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        if user.is_vip == 0:
            raise HTTPException(status_code=403, detail="只有VIP用户才能使用声音克隆功能")
        
        # 2. 保存录音文件
        audio_file_path = voice_clone_service.save_audio_sample(user_id, audio_file)
        
        # 3. 调用API克隆声音
        voice_id = voice_clone_service.clone_voice(user_id, audio_file_path)
        
        # 4. 保存声音样本记录
        voice_sample = VoiceSample(
            user_id=user_id,
            audio_url=audio_file_path
        )
        db.add(voice_sample)
        
        # 5. 更新用户的voice_id
        user.voice_id = voice_id
        db.commit()
        
        return {
            "code": 0,
            "message": "声音克隆成功",
            "data": {
                "voice_id": voice_id,
                "user_id": user_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"声音克隆失败: {str(e)}")
