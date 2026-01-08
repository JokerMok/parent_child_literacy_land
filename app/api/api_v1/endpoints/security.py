from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import requests
import json

from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

# 文本内容安全检查
@router.post("/check-text")
async def check_text(
    text: str,
    db: Session = Depends(get_db)
):
    """检查文本内容是否安全"""
    try:
        # 调用微信内容安全API
        access_token = await get_wechat_access_token()
        
        response = requests.post(
            settings.WECHAT_MSG_SEC_CHECK_URL,
            params={"access_token": access_token},
            json={"content": text}
        )
        
        result = response.json()
        
        if result["errcode"] == 0:
            return {"safe": True, "message": "文本内容安全"}
        else:
            return {"safe": False, "message": f"文本内容不安全: {result['errmsg']}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内容检查失败: {str(e)}")

# 图片内容安全检查
@router.post("/check-image")
async def check_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """检查图片内容是否安全"""
    try:
        # 读取文件内容
        image_content = await file.read()
        
        # 调用微信内容安全API
        access_token = await get_wechat_access_token()
        
        response = requests.post(
            settings.WECHAT_IMG_SEC_CHECK_URL,
            params={"access_token": access_token},
            files={"media": image_content}
        )
        
        result = response.json()
        
        if result["errcode"] == 0:
            return {"safe": True, "message": "图片内容安全"}
        else:
            return {"safe": False, "message": f"图片内容不安全: {result['errmsg']}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内容检查失败: {str(e)}")

# 获取微信访问令牌（内部函数）
async def get_wechat_access_token():
    """获取微信API访问令牌"""
    try:
        response = requests.get(
            "https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": settings.WECHAT_APPID,
                "secret": settings.WECHAT_SECRET
            }
        )
        
        result = response.json()
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"获取微信访问令牌失败: {result['errmsg']}")
    except Exception as e:
        raise Exception(f"获取微信访问令牌失败: {str(e)}")
