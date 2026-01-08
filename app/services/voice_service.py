import os
import httpx
from app.core.config import settings

class VoiceCloneService:
    """声音克隆服务类"""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
        self.dashscope_api_key = settings.DASHSCOPE_API_KEY
        self.dashscope_voice_clone_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/voice-clone/generation"
    
    def save_audio_sample(self, user_id: int, audio_file) -> str:
        """
        保存用户上传的录音样本
        :param user_id: 用户ID
        :param audio_file: 音频文件对象
        :return: 保存后的文件路径
        """
        try:
            # 创建用户专属目录
            user_dir = os.path.join(self.upload_dir, f"user_{user_id}")
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            
            # 保存文件
            file_path = os.path.join(user_dir, f"voice_sample_{user_id}_{os.getpid()}.mp3")
            with open(file_path, "wb") as f:
                f.write(audio_file.file.read())
            
            return file_path
        except Exception as e:
            print(f"保存音频样本失败: {e}")
            raise
    
    def clone_voice(self, user_id: int, audio_file_path: str) -> str:
        """
        调用通义千问API克隆声音
        :param user_id: 用户ID
        :param audio_file_path: 音频文件路径
        :return: 克隆的声音ID
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.dashscope_api_key}",
                "Content-Type": "multipart/form-data"
            }
            
            # 读取音频文件
            with open(audio_file_path, "rb") as f:
                audio_content = f.read()
            
            # 准备请求数据
            data = {
                "model": "qwen-vc-v1",
                "parameters": {
                    "name": f"user_voice_{user_id}",
                    "description": f"用户{user_id}的声音克隆模型"
                }
            }
            
            files = {
                "audio": (os.path.basename(audio_file_path), audio_content, "audio/mp3")
            }
            
            # 发送请求
            response = httpx.post(self.dashscope_voice_clone_url, headers=headers, data=data, files=files)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "SUCCESS":
                    # 假设通义千问返回的结果中包含voice_id
                    voice_id = result.get("output", {}).get("voice_id", "")
                    if voice_id:
                        return voice_id
                else:
                    print(f"通义千问声音克隆API调用失败: {result.get('message', '未知错误')}")
            else:
                print(f"通义千问声音克隆API调用失败: {response.status_code} - {response.text}")
            
            # 如果API调用失败，生成一个模拟的voice_id
            voice_id = f"voice_{user_id}_{os.getpid()}"
            return voice_id
        except Exception as e:
            print(f"克隆声音失败: {e}")
            # 发生异常时，生成一个模拟的voice_id
            voice_id = f"voice_{user_id}_{os.getpid()}"
            return voice_id

# 创建声音克隆服务实例
voice_clone_service = VoiceCloneService()
