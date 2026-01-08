from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "亲子识字乐园"
    PROJECT_VERSION: str = "1.0.0"
    
    # API配置
    API_V1_STR: str = "/api"
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/parent_child_literacy?charset=utf8mb4"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key"  # 在生产环境中应该使用环境变量
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 文件存储配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # AI服务配置
    AI_VISION_API_KEY: str = "your-aliyun-qwen-vl-api-key"
    
    # 通义千问TTS配置
    DASHSCOPE_API_KEY: str = "your-dashscope-api-key"
    
    # 微信小程序配置
    WECHAT_APPID: str = "your-wechat-appid"
    WECHAT_SECRET: str = "your-wechat-secret"
    
    # 内容安全配置
    WECHAT_MSG_SEC_CHECK_URL: str = "https://api.weixin.qq.com/wxa/msg_sec_check"
    WECHAT_IMG_SEC_CHECK_URL: str = "https://api.weixin.qq.com/wxa/img_sec_check"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
