import os
from datetime import datetime

# 导入各个模块
from user_profile import load_or_init_child_info, reset_child_info
from story_generator import build_prompt, select_story_summary, generate_story
from serial_story import (
    load_serial_story, save_serial_story, show_serial_story_info, 
    generate_serial_story_chapter, SERIAL_STORY_FILE
)
from tts import generate_audio_file
from utils import get_setting_choice, get_story_type, get_character_info, get_story_elements

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
        story_type = get_story_type()

        # 场景选择
        setting = get_setting_choice()
        
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
        
        # 输入主角信息
        character = get_character_info(setting)
        elements = get_story_elements()

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
            
            # 询问是否需要语音合成
            tts_choice = input("是否需要将故事转换为语音？(y/n)：").strip().lower()
            if tts_choice == 'y':
                generate_audio_file(story, "story")
        
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
                
                # 询问是否需要语音合成
                tts_choice = input("是否需要将这一章转换为语音？(y/n)：").strip().lower()
                if tts_choice == 'y':
                    generate_audio_file(chapter, "chapter1")
            return

    except ValueError as e:
        print(f"错误：{str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")
        print("请检查网络连接和API配置是否正确。")

if __name__ == "__main__":
    main() 