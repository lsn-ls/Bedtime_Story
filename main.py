import os
import json
from datetime import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Azure OpenAI 客户端初始化
try:
    client = AzureOpenAI(
        api_version="xxxx",
        azure_endpoint="xxxx",
        api_key="xxxx"
    )
except Exception as e:
    print(f"初始化客户端失败: {str(e)}")
    exit(1)

# 孩子信息记录文件
CHILD_INFO_FILE = "child_info.json"
# 连续剧记录文件
SERIAL_STORY_FILE = "serial_story.json"

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

# 年龄段判断与提示模板
def convert_months_to_prompt_info(months: int):
    if months <= 36:
        return 2, "100 到 300", "- 使用非常简单的词汇和句子\n- 重复句式，有节奏感，适合朗读\n- 内容温柔，没有复杂情节"
    elif months <= 60:
        return 4, "300 到 600", "- 语言简单清晰，加入基础情节\n- 有角色简单互动和因果关系\n- 风格温和、结局温馨"
    else:
        return 6, "600 到 1000", "- 故事情节稍复杂，加入冲突与解决\n- 增加对话和情感表达\n- 故事结构完整，寓意积极向上"

# Prompt 构建器
def build_prompt(months: int, character: str, elements: str, setting: str) -> str:
    age_display, word_limit, style_notes = convert_months_to_prompt_info(months)
    prompt = f"""你是一个有爱心的儿童故事作家，请为一个{age_display}岁的孩子创作一个睡前故事。\n
故事主角名字叫：{character}。\n故事应包含元素：{elements}。\n故事发生在：{setting}。\n
请严格遵守以下要求：
- 字数控制在{word_limit}字之间
- {style_notes}
- 内容积极健康，适合儿童阅读
- 结局温馨美好
- 不要包含恐怖、暴力、消极等内容
- 用中文输出故事，分段清晰，适合朗读\n"""
    return prompt

def generate_story_summaries(prompt: str) -> list:
    """生成故事概要列表"""
    try:
        print("正在生成故事概要...")
        print("提示：正在连接AI服务，这可能需要几秒钟时间...")
        
        response = client.chat.completions.create(
            model="SL-Azure-gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的儿童故事策划人。请确保每个故事概要控制在40-60个字之间。"},
                {"role": "user", "content": prompt + "\n请根据上述要求生成三个不同方向的故事概要，要求：\n1. 每个概要控制在40-60个字之间\n2. 用数字编号（1. 2. 3.）分别列出三个概要\n3. 每个概要应该包含：主角、场景、主要情节和结局\n4. 确保三个概要风格统一，但内容各不相同\n5. 请仔细检查字数，确保每个概要都在40-60个字之间"}
            ],
            max_tokens=500,
            temperature=0.8,
            top_p=0.95
        )
        
        if not response or not response.choices:
            print("错误：AI服务返回空响应")
            return []
            
        content = response.choices[0].message.content.strip()
        print("\nAI返回的原始内容：")
        print(content)
        print("\n正在解析故事概要...")
        
        # 优化概要解析逻辑
        summaries = []
        current_summary = []
        
        for line in content.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是新的概要开始（以数字开头）
            if line[0].isdigit() and line[1:3] in [". ", "、", "．"]:
                if current_summary:
                    summary_text = " ".join(current_summary)
                    char_count = len(''.join(c for c in summary_text if c.strip()))
                    print(f"发现概要，字数：{char_count}")
                    summaries.append(summary_text)
                current_summary = [line[3:].strip()]
            else:
                current_summary.append(line)
        
        # 添加最后一个概要
        if current_summary:
            summary_text = " ".join(current_summary)
            char_count = len(''.join(c for c in summary_text if c.strip()))
            print(f"发现概要，字数：{char_count}")
            summaries.append(summary_text)
        
        # 确保只返回三个概要，并且每个概要都在40-60个字之间
        if len(summaries) >= 3:
            # 检查每个概要的字数
            valid_summaries = []
            for i, summary in enumerate(summaries[:3], 1):
                # 移除所有标点符号和空格后计算字数
                char_count = len(''.join(c for c in summary if c.strip()))
                print(f"概要{i}字数：{char_count}")
                if 40 <= char_count <= 60:
                    valid_summaries.append(summary)
                else:
                    print(f"概要{i}字数不符合要求（当前{char_count}字），需要重新生成")
                    return generate_story_summaries(prompt)
            
            if len(valid_summaries) == 3:
                print("成功生成三个符合要求的概要！")
                return valid_summaries
            else:
                print(f"概要数量不足（当前{len(valid_summaries)}个），需要重新生成")
                return generate_story_summaries(prompt)
        else:
            print(f"生成的概要数量不足（当前{len(summaries)}个），需要重新生成")
            return generate_story_summaries(prompt)
            
    except Exception as e:
        print(f"生成故事概要时发生错误：{str(e)}")
        print("错误类型：", type(e).__name__)
        import traceback
        print("错误详情：")
        print(traceback.format_exc())
        return []

def select_story_summary(prompt: str) -> str:
    """让用户选择或重新生成故事概要"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        print(f"\n尝试生成故事概要（第{retry_count + 1}次）...")
        summaries = generate_story_summaries(prompt)
        
        if not summaries:
            retry_count += 1
            if retry_count < max_retries:
                print(f"生成失败，将在3秒后重试...")
                import time
                time.sleep(3)
                continue
            else:
                print("多次尝试生成故事概要均失败，请检查网络连接或稍后重试。")
                return None
            
        print("\n=== 故事概要选项 ===")
        for i, summary in enumerate(summaries, 1):
            print(f"\n{i}. {summary}")
        
        print("\n请选择：")
        print("1-3: 选择对应的故事概要")
        print("0: 重新生成故事概要")
        print("q: 退出程序")
        
        choice = input("\n请输入您的选择: ").strip().lower()
        
        if choice == 'q':
            exit(0)
        elif choice == '0':
            print("\n正在重新生成故事概要...")
            continue
        elif choice in ['1', '2', '3']:
            return summaries[int(choice) - 1]
        else:
            print("无效的选择，请重试。")
    
    return None

# 故事生成器
def generate_story(prompt: str) -> str:
    try:
        print("正在连接Azure OpenAI服务...")
        response = client.chat.completions.create(
            model="SL-Azure-gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "你是一个温柔的儿童故事作家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.8,
            top_p=0.95
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return "抱歉，故事生成失败，请稍后重试。"

def reset_child_info():
    """重置孩子信息"""
    if os.path.exists(CHILD_INFO_FILE):
        os.remove(CHILD_INFO_FILE)
        print("已重置孩子信息。")
    else:
        print("没有找到孩子信息记录。")
    
    # 重置连续剧信息
    if os.path.exists(SERIAL_STORY_FILE):
        os.remove(SERIAL_STORY_FILE)
        print("已重置连续剧信息。")
    else:
        print("没有找到连续剧信息记录。")

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
        
        response = client.chat.completions.create(
            model="SL-Azure-gpt-4.1",
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

def main():
    try:
        # 检查是否需要重置信息
        print("\n提示：输入 'r' 可以重置孩子信息（年龄和性别）")
        reset_choice = input("是否需要重置孩子信息？(y/n，直接回车继续)：").strip().lower()
        if reset_choice == 'y':
            reset_child_info()
            print("请重新输入孩子信息。")
        
        current_months, gender = load_or_init_child_info()

        # 选择故事类型
        print("\n请选择故事类型：")
        print("1. 单元剧（独立故事）")
        print("2. 连续剧（分章节的长篇故事，共28章）")
        
        while True:
            try:
                story_type = int(input("\n请输入选择（1-2）：").strip())
                if story_type in [1, 2]:
                    break
                else:
                    print("无效的选择，请输入1或2。")
            except ValueError:
                print("请输入有效的数字。")

        # 场景选择
        valid_settings = ["森林", "城堡", "海洋", "玩具世界", "牧场", "太空"]
        print("\n请选择故事场景：")
        for i, setting in enumerate(valid_settings, 1):
            print(f"{i}. {setting}")
        
        while True:
            try:
                choice = int(input("\n请输入场景编号（1-6）：").strip())
                if 1 <= choice <= 6:
                    setting = valid_settings[choice - 1]
                    print(f"\n已选择场景：{setting}")
                    modify_choice = input("请确认场景？(y/n，直接回车继续)：").strip().lower()
                    if modify_choice == 'y':
                        continue
                    break
                else:
                    print("无效的选择，请输入1-6之间的数字。")
            except ValueError:
                print("请输入有效的数字。")
        
        # 根据场景提示合适的主角属性
        setting_prompts = {
            "森林": "（如：小兔子、小松鼠、小鹿）",
            "城堡": "（如：小王子、小公主、小骑士）",
            "海洋": "（如：小海豚、小海龟、小章鱼）",
            "玩具世界": "（如：小木偶、小布熊、小机器人）",
            "牧场": "（如：小羊、小牛、小马）",
            "太空": "（如：小星星、小火箭、小宇航员）"
        }
        
        # 检查是否有未完成的连续剧
        serial_story = load_serial_story()
        
        # 如果选择了连续剧，并且有未完成的故事，且场景相同
        if story_type == 2 and serial_story and serial_story['setting'] == setting:
            print("\n发现相同场景的连续剧！")
            print(f"上次的主角：{serial_story['character']}")
            print(f"上次的故事元素：{serial_story['elements']}")
            
            # 检查是否已经完成28章
            if serial_story['current_chapter'] >= 28:
                print("\n这个故事已完结！")
                print("\n请选择：")
                print("1. 重新阅读这个故事")
                print("2. 生成一个全新的故事")
                print("3. 查看完整故事内容")
                
                while True:
                    try:
                        choice = int(input("\n请输入选择（1-3）：").strip())
                        if choice in [1, 2, 3]:
                            break
                        else:
                            print("无效的选择，请输入1-3之间的数字。")
                    except ValueError:
                        print("请输入有效的数字。")
                
                if choice == 1:  # 重新阅读
                    print("\n=== 完整故事内容 ===")
                    print(f"\n故事梗概：\n{serial_story['story_summary']}\n")
                    for i, chapter in enumerate(serial_story['chapters'], 1):
                        print(f"\n第{i}章：")
                        print(chapter)
                    return
                
                elif choice == 3:  # 查看完整故事
                    print("\n=== 完整故事内容 ===")
                    print(f"\n故事梗概：\n{serial_story['story_summary']}\n")
                    for i, chapter in enumerate(serial_story['chapters'], 1):
                        print(f"\n第{i}章：")
                        print(chapter)
                    return
                
                # 如果选择2（生成新故事）或不是相同的故事类型，继续执行下面的代码
            else:
                print("\n请选择：")
                print("1. 继续这个故事")
                print("2. 重新生成新故事")
                print("3. 查看完整故事内容")
                
                while True:
                    try:
                        choice = int(input("\n请输入选择（1-3）：").strip())
                        if choice in [1, 2, 3]:
                            break
                        else:
                            print("无效的选择，请输入1-3之间的数字。")
                    except ValueError:
                        print("请输入有效的数字。")
                
                if choice == 1:  # 继续故事
                    # 使用已保存的角色和场景信息
                    character = serial_story['character']
                    elements = serial_story['elements']
                    base_prompt = build_prompt(current_months, character, elements, setting)
                    
                    # 生成下一章
                    chapter = generate_serial_story_chapter(
                        base_prompt,
                        serial_story['current_chapter'] + 1,
                        serial_story['chapters'],
                        serial_story['story_summary']
                    )
                    if chapter:
                        serial_story['chapters'].append(chapter)
                        serial_story['current_chapter'] += 1
                        save_serial_story(serial_story)
                        print(f"\n=== 第{serial_story['current_chapter']}章 ===\n{chapter}\n")
                    return
                
                elif choice == 3:  # 查看完整故事
                    print("\n=== 完整故事内容 ===")
                    print(f"\n故事梗概：\n{serial_story['story_summary']}\n")
                    for i, chapter in enumerate(serial_story['chapters'], 1):
                        print(f"\n第{i}章：")
                        print(chapter)
                    return
        
        # 输入主角属性
        character_type = input(f"请输入主角属性{setting_prompts[setting]}：").strip()
        # 输入主角名字
        character_name = input(f"请为主角{character_type}起一个名字：").strip()
        # 组合主角信息
        character = f"{character_type}{character_name}"
        
        elements = input("请输入故事元素（如：友谊、勇气、音乐）：").strip()

        # 生成基础prompt
        base_prompt = build_prompt(current_months, character, elements, setting)

        if story_type == 1:  # 单元剧
            # 选择故事概要
            selected_summary = select_story_summary(base_prompt)
            
            # 根据选择的概要生成完整故事
            final_prompt = base_prompt + f"\n请根据以下故事概要展开创作：\n{selected_summary}"

            print("\n正在生成故事，请稍候...\n")
            story = generate_story(final_prompt)
            print("=== 睡前故事 ===\n" + story + "\n")
        
        else:  # 连续剧
            # 开始新的连续剧
            print("\n开始创建新的连续剧...")
            print("注意：连续剧共28章，每章都会保持故事的连贯性。")
            
            # 选择故事概要
            selected_summary = select_story_summary(base_prompt)
            
            # 创建新的连续剧
            serial_story = {
                "character": character,
                "setting": setting,
                "elements": elements,
                "current_chapter": 1,
                "chapters": [],
                "story_summary": selected_summary
            }
            
            # 生成第一章
            chapter = generate_serial_story_chapter(base_prompt, 1, [], selected_summary)
            if chapter:
                serial_story['chapters'].append(chapter)
                save_serial_story(serial_story)
                print("\n=== 第1章 ===\n" + chapter + "\n")
            return

    except ValueError as e:
        print(f"错误：{str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")
        print("请检查网络连接和API配置是否正确。")

if __name__ == "__main__":
    main() 
