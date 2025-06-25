"""
serial_story.py
连续剧进度管理相关逻辑
"""

import os
import json
import openai
from dotenv import load_dotenv
from typing import Dict, List, Optional

# 加载环境变量
load_dotenv()

# Azure OpenAI 配置
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# 连续剧记录文件
SERIAL_STORY_FILE = "serial_story.json"

def load_serial_story() -> dict:
    """加载连续剧信息"""
    if os.path.exists(SERIAL_STORY_FILE):
        with open(SERIAL_STORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_serial_story(story_data: dict):
    """保存连续剧信息"""
    with open(SERIAL_STORY_FILE, "w", encoding="utf-8") as f:
        json.dump(story_data, f, ensure_ascii=False, indent=2)

def show_serial_story_info(serial_story: dict):
    """显示连续剧信息"""
    print("\n=== 当前连续剧信息 ===")
    print(f"主角：{serial_story['character']}")
    print(f"场景：{serial_story['setting']}")
    print(f"故事元素：{serial_story['elements']}")
    print(f"当前进度：第{serial_story['current_chapter']}章 / 共28章")
    print("\n已生成章节：")
    for i, chapter in enumerate(serial_story['chapters'], 1):
        print(f"\n第{i}章：")
        print(chapter[:100] + "..." if len(chapter) > 100 else chapter)

def generate_serial_story_chapter(prompt: str, chapter_num: int, previous_chapters: list, story_summary: str = None) -> str:
    """生成连续剧的章节"""
    try:
        if chapter_num > 28:
            print("\n故事已经完成28章，可以开始新的故事了！")
            return None
            
        print(f"\n正在生成第{chapter_num}章...")
        chapter_prompt = f"{prompt}\n\n这是第{chapter_num}章，总共28章。"
        
        # 添加故事梗概
        if story_summary:
            chapter_prompt += f"\n\n故事梗概：\n{story_summary}"
            
        if previous_chapters:
            chapter_prompt += "\n\n前文概要：\n" + "\n".join(previous_chapters)
        
        # 根据章节数调整提示
        if chapter_num == 1:
            chapter_prompt += "\n这是第一章，请为整个故事做好铺垫，介绍主要角色和背景。"
        elif chapter_num == 28:
            chapter_prompt += "\n这是最后一章，请为整个故事画上圆满的句号，确保所有情节都得到妥善解决。"
        else:
            chapter_prompt += "\n请继续发展故事情节，注意与前文的连贯性，并为下一章留下伏笔。"
        
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": "你是一个专业的儿童故事作家，擅长创作连续剧式的故事。请确保故事适合儿童阅读，内容积极向上。"},
                {"role": "user", "content": chapter_prompt}
            ],
            max_tokens=1024,
            temperature=0.8,
            top_p=0.95
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"生成章节失败：{str(e)}")
        return None 