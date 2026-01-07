import os
import asyncio
import httpx
from app.core.config import settings

class TTSService:
    """TTS服务类"""
    
    def __init__(self):
        self.dashscope_api_key = settings.DASHSCOPE_API_KEY
        self.dashscope_tts_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-to-speech/generation"
    
    async def generate_voice_qwen(self, text: str, voice_id: str = "longxiaochun", output_file: str = "output.mp3") -> bool:
        """
        使用通义千问TTS生成语音
        :param text: 要转换的文本
        :param voice_id: 声音ID，默认使用小纯的声音
        :param output_file: 输出文件路径
        :return: 是否成功
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.dashscope_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "qwen-t2a-v1",
                "input": {
                    "text": text
                },
                "parameters": {
                    "voice": voice_id,
                    "format": "mp3",
                    "sample_rate": 24000
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.dashscope_tts_url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "SUCCESS":
                        audio_url = result.get("output", {}).get("audio", "")
                        if audio_url:
                            # 下载音频文件
                            audio_response = await client.get(audio_url)
                            if audio_response.status_code == 200:
                                with open(output_file, "wb") as f:
                                    f.write(audio_response.content)
                                return True
                else:
                    print(f"通义千问TTS API调用失败: {response.status_code} - {response.text}")
            
            return False
        except Exception as e:
            print(f"通义千问TTS生成失败: {e}")
            return False
    
    async def generate_voice_cloned(self, text: str, voice_id: str, output_file: str) -> bool:
        """
        使用克隆的声音生成语音（通义千问API）
        :param text: 要转换的文本
        :param voice_id: 克隆的声音ID
        :param output_file: 输出文件路径
        :return: 是否成功
        """
        try:
            # 使用通义千问TTS API，voice_id作为自定义声音ID
            return await self.generate_voice_qwen(text, voice_id, output_file)
        except Exception as e:
            print(f"克隆声音生成失败: {e}")
            return False
    
    async def synthesize(self, text: str, voice_id: str = "", output_file: str = "output.mp3") -> bool:
        """
        语音合成统一接口
        :param text: 要转换的文本
        :param voice_id: 克隆的声音ID（可选）
        :param output_file: 输出文件路径
        :return: 是否成功
        """
        if voice_id:
            # 使用克隆声音
            return await self.generate_voice_cloned(text, voice_id, output_file)
        else:
            # 使用默认通义千问TTS
            return await self.generate_voice_qwen(text, output_file=output_file)

# 创建TTS服务实例
tts_service = TTSService()
