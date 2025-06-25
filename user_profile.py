"""
user_profile.py
孩子信息管理相关逻辑
"""

import os
import json
from typing import Tuple
from datetime import datetime

# 孩子信息记录文件
CHILD_INFO_FILE = "child_info.json"

def get_elapsed_months(start_date: str) -> int:
    """计算从 start_date 到今天过了多少个月"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    now = datetime.now()
    return (now.year - start.year) * 12 + (now.month - start.month)

def load_or_init_child_info() -> tuple:
    """读取或初始化孩子信息（年龄和性别）"""
    if os.path.exists(CHILD_INFO_FILE):
        with open(CHILD_INFO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        base_months = data["base_months"]
        start_date = data["start_date"]
        gender = data.get("gender", "")
        elapsed = get_elapsed_months(start_date)
        total_months = base_months + elapsed
        print(f"[自动识别] 当前孩子月龄为：{total_months}个月")
        if gender:
            print(f"[自动识别] 孩子性别为：{gender}")
        return total_months, gender
    else:
        print("欢迎使用儿童故事生成器！请先输入孩子信息。")
        age_input = input("请输入孩子当前年龄（如：3岁6个月）：").strip()
        import re
        match = re.match(r'(\d+)\s*岁\s*(\d+)?\s*个月?', age_input)
        if match:
            years = int(match.group(1))
            months = int(match.group(2) or 0)
            total_months = years * 12 + months
            now_str = datetime.now().strftime("%Y-%m-%d")
            gender = input("请输入孩子性别（男/女）：").strip()
            with open(CHILD_INFO_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "start_date": now_str,
                    "base_months": total_months,
                    "gender": gender
                }, f, ensure_ascii=False, indent=2)
            print(f"[记录完成] 初始月龄：{total_months}个月，性别：{gender}，记录时间：{now_str}")
            return total_months, gender
        else:
            raise ValueError('输入格式有误，请输入如"3岁6个月"')

def reset_child_info():
    """重置孩子信息"""
    if os.path.exists(CHILD_INFO_FILE):
        os.remove(CHILD_INFO_FILE)
        print("已重置孩子信息。")
    else:
        print("没有找到孩子信息记录。")
    
    # 重置连续剧信息
    SERIAL_STORY_FILE = "serial_story.json"
    if os.path.exists(SERIAL_STORY_FILE):
        os.remove(SERIAL_STORY_FILE)
        print("已重置连续剧信息。")
    else:
        print("没有找到连续剧信息记录。") 