"""
story_generator.py
AI故事生成与概要生成相关逻辑
"""

import openai
import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Azure OpenAI 配置
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# 这里可以放置生成故事概要、生成完整故事等函数

def convert_months_to_prompt_info(months: int):
    """年龄段判断与提示模板"""
    if months <= 36:
        return 2, "400 到 600", "- 使用非常简单的词汇和句子\n- 重复句式，有节奏感，适合朗读\n- 内容温柔，没有复杂情节"
    elif months <= 60:
        return 4, "600 到 1000", "- 语言简单清晰，加入基础情节\n- 有角色简单互动和因果关系\n- 风格温和、结局温馨"
    else:
        return 6, "1000 到 1500", "- 故事情节稍复杂，加入冲突与解决\n- 增加对话和情感表达\n- 故事结构完整，寓意积极向上"

def build_prompt(months: int, character: str, elements: str, setting: str) -> str:
    """Prompt 构建器"""
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
        
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
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

def generate_story(prompt: str) -> str:
    """故事生成器"""
    try:
        print("正在连接Azure OpenAI服务...")
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
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