"""
utils.py
通用工具函数
"""

from datetime import datetime
from typing import Any

def get_elapsed_months(start_date: str) -> int:
    # 从 main.py 迁移的计算月龄函数
    pass

def convert_months_to_prompt_info(months: int):
    # 从 main.py 迁移的年龄段判断与提示模板函数
    pass 

# 场景选择相关常量
VALID_SETTINGS = ["森林", "城堡", "海洋", "玩具世界", "牧场", "太空"]

SETTING_PROMPTS = {
    "森林": "（如：小兔子、小松鼠、小鹿）",
    "城堡": "（如：小王子、小公主、小骑士）",
    "海洋": "（如：小海豚、小海龟、小章鱼）",
    "玩具世界": "（如：小木偶、小布熊、小机器人）",
    "牧场": "（如：小羊、小牛、小马）",
    "太空": "（如：小星星、小火箭、小宇航员）"
}

def get_setting_choice() -> str:
    """获取用户选择的场景"""
    print("\n请选择故事场景：")
    for i, setting in enumerate(VALID_SETTINGS, 1):
        print(f"{i}. {setting}")
    
    while True:
        try:
            choice = int(input("\n请输入场景编号（1-6）：").strip())
            if 1 <= choice <= 6:
                setting = VALID_SETTINGS[choice - 1]
                print(f"\n已选择场景：{setting}")
                modify_choice = input("是否进行修改？(y/n，直接回车继续)：").strip().lower()
                if modify_choice == 'y':
                    continue
                return setting
            else:
                print("无效的选择，请输入1-6之间的数字。")
        except ValueError:
            print("请输入有效的数字。")

def get_story_type() -> int:
    """获取用户选择的故事类型"""
    print("\n请选择故事类型：")
    print("1. 单元剧（独立故事）")
    print("2. 连续剧（分章节的长篇故事，共28章）")
    
    while True:
        try:
            story_type = int(input("\n请输入选择（1-2）：").strip())
            if story_type in [1, 2]:
                return story_type
            else:
                print("无效的选择，请输入1或2。")
        except ValueError:
            print("请输入有效的数字。")

def get_character_info(setting: str) -> str:
    """获取主角信息"""
    # 输入主角属性
    character_type = input(f"请输入主角属性{SETTING_PROMPTS[setting]}：").strip()
    # 输入主角名字
    character_name = input(f"请为主角{character_type}起一个名字：").strip()
    # 组合主角信息
    return f"{character_type}{character_name}"

def get_story_elements() -> str:
    """获取故事元素"""
    return input("请输入故事元素（如：友谊、勇气、音乐）：").strip() 