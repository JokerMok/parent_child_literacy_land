import os
import json
import re
import asyncio
import time
from http import HTTPStatus
import dashscope
from dashscope import MultiModalConversation
import edge_tts

# ------------------------------------------------------------------
# 配置区
# ------------------------------------------------------------------
# 1. 阿里云 API Key
dashscope.api_key = "sk-02bcd8ba617e4a73909c74be62396b95"

# 2. 文件夹配置
SOURCE_IMAGE_DIR = "images"
AUDIO_DIR = "audio"
PADDING_RATIO = 0.02
MODEL_NAME = 'qwen3-vl-flash'

# 3. 服务器资源根路径 (用于生成音频URL)
# 确保这里是你服务器的真实地址
BASE_URL = "https://www.shizibandu.icu/miniprogram_assets"


# ------------------------------------------------------------------

def normalize_box(box_1000):
    x1, y1, x2, y2 = box_1000
    left = x1 / 1000;
    top = y1 / 1000
    right = x2 / 1000;
    bottom = y2 / 1000
    width = right - left;
    height = bottom - top
    w_pad = width * PADDING_RATIO * 2;
    h_pad = height * PADDING_RATIO * 2
    left = max(0, left - w_pad / 2);
    top = max(0, top - h_pad / 2)
    width = min(1.0, width + w_pad);
    height = min(1.0, height + h_pad)
    return [round(left, 4), round(top, 4), round(width, 4), round(height, 4)]


async def generate_audio(text):
    path = os.path.join(AUDIO_DIR, f"{text}.mp3")
    if os.path.exists(path): return
    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(path)
        print(f"      🎵 生成语音: {text}")
    except Exception as e:
        print(f"      ❌ 语音失败: {e}")


def parse_json(content):
    try:
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```', '', content)
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match: return json.loads(match.group(0))
    except:
        pass
    return None


def process_single_image(image_path):
    prompt = "请检测图中所有的【中文识字标签气泡】。返回JSON列表，含'text'和'box_2d'([xmin, ymin, xmax, ymax], 0-1000)。"
    messages = [{'role': 'user', 'content': [{'image': f'file://{os.path.abspath(image_path)}'}, {'text': prompt}]}]
    try:
        response = MultiModalConversation.call(model=MODEL_NAME, messages=messages)
        if response.status_code == HTTPStatus.OK:
            return parse_json(response.output.choices[0].message.content[0]['text'])
    except:
        pass
    return None


def main():
    if not os.path.exists(SOURCE_IMAGE_DIR):
        print(f"❌ 找不到 '{SOURCE_IMAGE_DIR}' 文件夹");
        return

    files = [f for f in os.listdir(SOURCE_IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"🚀 启动批量处理 (输出到 all_configs.json)")

    MASTER_CONFIG = {}
    audio_tasks = []
    os.makedirs(AUDIO_DIR, exist_ok=True)

    for i, file in enumerate(files):
        print(f"\n[{i + 1}/{len(files)}] 分析: {file} ...")
        key = os.path.splitext(file)[0]
        file_path = os.path.join(SOURCE_IMAGE_DIR, file)

        data = process_single_image(file_path)
        if not data: continue

        print(f"      ✅ 识别到 {len(data)} 个标签")
        scene_data = []
        for item in data:
            text = item.get('text', '').strip()
            box = item.get('box_2d')
            if not text or not box: continue

            # 关键修改：音频路径直接指向服务器
            audio_url = f"{BASE_URL}/assets/audio/{text}.mp3"

            scene_data.append({
                "text": text,
                "audio": audio_url,
                "rect": normalize_box(box)
            })
            audio_tasks.append(generate_audio(text))

        MASTER_CONFIG[key] = scene_data
        time.sleep(1)

    if audio_tasks:
        print(f"\n🎵 合成音频...")

        async def run_all():
            await asyncio.gather(*audio_tasks)

        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                asyncio.create_task(run_all())
            else:
                loop.run_until_complete(run_all())
        except RuntimeError:
            asyncio.run(run_all())

    # ---------------------------------------------------------
    # 关键修改：输出纯 JSON 文件 (不带 module.exports)
    # ---------------------------------------------------------
    with open("all_configs.json", "w", encoding="utf-8") as f:
        json.dump(MASTER_CONFIG, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 30)
    print("🎉 完成！请执行以下上传步骤：")
    print("1. 将 all_configs.json 上传到服务器: C:\\nginx\\html\\miniprogram_assets\\")
    print("2. 将 audio/ 里的文件上传到服务器: C:\\nginx\\html\\miniprogram_assets\\assets\\audio\\")


if __name__ == "__main__":
    main()