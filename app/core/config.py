from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "亲子识字乐园"
    PROJECT_VERSION: str = "1.0.0"
    
    # API配置
    API_V1_STR: str = "/api"
    
    # --------------------------------------------------------
    # 1. 数据库配置 (已改为你的真实账号密码)
    # --------------------------------------------------------
    # 格式: mysql+pymysql://用户名:密码@地址:端口/库名
    DATABASE_URL: str = "mysql+pymysql://jokermok:jokermok00@localhost:3306/parent_child_literacy?charset=utf8mb4"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-jokermok-2025" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # --------------------------------------------------------
    # 2. 文件存储配置 (关键！必须指向 Nginx 目录)
    # --------------------------------------------------------
    # 图片物理存储路径
    UPLOAD_DIR: str = r"C:\nginx\html\miniprogram_assets\uploads"
    # 音频物理存储路径 (Trae模板里没这个，我补上了，代码里可能会用到)
    AUDIO_DIR: str = r"C:\nginx\html\miniprogram_assets\assets\audio"
    
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 改为 20MB，防止高清图传不上
    
    # --------------------------------------------------------
    # 3. URL 前缀配置 (新增！给前端返回链接用)
    # --------------------------------------------------------
    UPLOAD_URL_PREFIX: str = "http://175.178.2.155/miniprogram_assets/uploads"
    AUDIO_URL_PREFIX: str = "http://175.178.2.155/miniprogram_assets/assets/audio"

    # --------------------------------------------------------
    # 4. API Key 配置 (已填入)
    # --------------------------------------------------------
    # AI服务配置 (视觉 + TTS)
    DASHSCOPE_API_KEY: str = "sk-02bcd8ba617e4a73909c74be62396b95"
    # 这里的 AI_VISION_API_KEY 如果 Trae 代码里用了单独的变量，也填一样的即可
    AI_VISION_API_KEY: str = "sk-02bcd8ba617e4a73909c74be62396b95"
    
    # 微信小程序配置
    WECHAT_APPID: str = "wx6da4b3363a54fb0a"
    WECHAT_SECRET: str = "12342fefb83c25f42bf85802db9b6245"
    
    # 内容安全配置
    WECHAT_MSG_SEC_CHECK_URL: str = "https://api.weixin.qq.com/wxa/msg_sec_check"
    WECHAT_IMG_SEC_CHECK_URL: str = "https://api.weixin.qq.com/wxa/img_sec_check"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# 自动创建目录
if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)
if not os.path.exists(settings.AUDIO_DIR):
    os.makedirs(settings.AUDIO_DIR)