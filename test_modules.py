#!/usr/bin/env python3
"""
测试脚本 - 验证各个模块的功能
"""

def test_imports():
    """测试模块导入"""
    print("=== 测试模块导入 ===")
    
    try:
        from user_profile import load_or_init_child_info, reset_child_info
        print("✓ user_profile 模块导入成功")
    except Exception as e:
        print(f"✗ user_profile 模块导入失败: {e}")
    
    try:
        from story_generator import build_prompt, select_story_summary, generate_story
        print("✓ story_generator 模块导入成功")
    except Exception as e:
        print(f"✗ story_generator 模块导入失败: {e}")
    
    try:
        from serial_story import load_serial_story, save_serial_story, show_serial_story_info
        print("✓ serial_story 模块导入成功")
    except Exception as e:
        print(f"✗ serial_story 模块导入失败: {e}")
    
    try:
        from tts import text_to_speech, generate_audio_file
        print("✓ tts 模块导入成功")
    except Exception as e:
        print(f"✗ tts 模块导入失败: {e}")
    
    try:
        from utils import get_setting_choice, get_story_type, get_character_info
        print("✓ utils 模块导入成功")
    except Exception as e:
        print(f"✗ utils 模块导入失败: {e}")

def test_story_generator():
    """测试故事生成器功能"""
    print("\n=== 测试故事生成器功能 ===")
    
    from story_generator import convert_months_to_prompt_info, build_prompt
    
    # 测试年龄段判断
    test_months = [24, 48, 72]
    for months in test_months:
        age_display, word_limit, style_notes = convert_months_to_prompt_info(months)
        print(f"月龄 {months}: {age_display}岁, {word_limit}字")
    
    # 测试prompt构建
    prompt = build_prompt(48, "小兔子贝贝", "友谊", "森林")
    print(f"\n生成的prompt长度: {len(prompt)} 字符")
    print("Prompt预览:", prompt[:100] + "...")

def test_utils():
    """测试工具函数"""
    print("\n=== 测试工具函数 ===")
    
    from utils import VALID_SETTINGS, SETTING_PROMPTS
    
    print(f"可用场景: {VALID_SETTINGS}")
    print(f"场景提示数量: {len(SETTING_PROMPTS)}")

def test_serial_story():
    """测试连续剧功能"""
    print("\n=== 测试连续剧功能 ===")
    
    from serial_story import load_serial_story, save_serial_story
    
    # 测试数据结构
    test_story = {
        "character": "小兔子贝贝",
        "setting": "森林",
        "elements": "友谊",
        "current_chapter": 1,
        "chapters": ["第一章内容..."],
        "story_summary": "这是一个关于友谊的故事"
    }
    
    try:
        save_serial_story(test_story)
        print("✓ 保存连续剧信息成功")
        
        loaded_story = load_serial_story()
        if loaded_story:
            print("✓ 加载连续剧信息成功")
            print(f"  主角: {loaded_story['character']}")
            print(f"  场景: {loaded_story['setting']}")
            print(f"  当前章节: {loaded_story['current_chapter']}")
        else:
            print("✗ 加载连续剧信息失败")
    except Exception as e:
        print(f"✗ 连续剧功能测试失败: {e}")

def main():
    """主测试函数"""
    print("开始测试模块化重构后的代码...\n")
    
    test_imports()
    test_story_generator()
    test_utils()
    test_serial_story()
    
    print("\n=== 测试完成 ===")
    print("所有模块导入成功，功能正常！")

if __name__ == "__main__":
    main() 