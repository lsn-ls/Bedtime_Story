"""
tts.py
语音合成相关逻辑
"""

import edge_tts
import asyncio
from typing import Optional

async def text_to_speech(text: str, output_file: str):
    """将文本转换为语音"""
    try:
        # 使用中文女声
        voice = "zh-CN-XiaoxiaoNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        print(f"\n语音文件已保存为：{output_file}")
    except Exception as e:
        print(f"语音合成失败：{str(e)}")

def generate_audio_file(text: str, prefix: str = "story") -> str:
    """生成音频文件并返回文件名"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{prefix}_{timestamp}.mp3"
    
    print("\n正在生成语音，请稍候...")
    # 运行语音合成
    asyncio.run(text_to_speech(text, output_file))
    return output_file 