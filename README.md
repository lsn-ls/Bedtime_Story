# 儿童睡前故事生成器

一个基于 Azure OpenAI 的智能儿童睡前故事生成器，支持单元剧和连续剧两种模式，并具备文本转语音功能。

## 功能特点

- 🎯 **年龄适配**: 根据孩子年龄自动调整故事难度和长度
- 📚 **双模式**: 支持单元剧（独立故事）和连续剧（28章长篇故事）
- 🎭 **场景丰富**: 提供6种不同场景（森林、城堡、海洋、玩具世界、牧场、太空）
- 🎨 **个性化**: 自定义主角和故事元素
- 🔊 **语音合成**: 支持将故事转换为语音文件
- 💾 **进度保存**: 自动保存连续剧进度和孩子信息
- 🔄 **智能续写**: 连续剧支持断点续写功能

## 项目结构

```
Bedtime_Story/
├── main.py              # 主程序入口
├── user_profile.py      # 用户配置文件管理
├── story_generator.py   # 故事生成核心功能
├── serial_story.py      # 连续剧管理功能
├── tts.py              # 文本转语音功能
├── utils.py            # 工具函数和常量
├── test_modules.py     # 模块测试脚本
├── requirements.txt    # 依赖包列表
├── README.md          # 项目说明文档
└── child_age.json     # 孩子年龄配置文件
```

## 模块说明

### `main.py` - 主程序
- 程序入口点
- 协调各个模块的功能
- 处理用户交互流程

### `user_profile.py` - 用户配置管理
- `load_or_init_child_info()`: 加载或初始化孩子信息
- `reset_child_info()`: 重置孩子和连续剧信息
- `get_elapsed_months()`: 计算孩子月龄

### `story_generator.py` - 故事生成核心
- `build_prompt()`: 构建AI提示词
- `generate_story_summaries()`: 生成故事概要
- `select_story_summary()`: 用户选择故事概要
- `generate_story()`: 生成完整故事
- `convert_months_to_prompt_info()`: 年龄段判断

### `serial_story.py` - 连续剧管理
- `load_serial_story()`: 加载连续剧信息
- `save_serial_story()`: 保存连续剧信息
- `show_serial_story_info()`: 显示连续剧信息
- `generate_serial_story_chapter()`: 生成连续剧章节

### `tts.py` - 文本转语音
- `text_to_speech()`: 异步语音合成
- `generate_audio_file()`: 生成音频文件

### `utils.py` - 工具函数
- `get_setting_choice()`: 获取场景选择
- `get_story_type()`: 获取故事类型
- `get_character_info()`: 获取主角信息
- `get_story_elements()`: 获取故事元素
- 场景和提示词常量定义

## 安装和配置

### 1. 环境要求
- Python 3.7+
- 虚拟环境（推荐）

### 2. 安装依赖
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

### 3. 配置环境变量
创建 `.env` 文件并配置以下变量：
```env
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

## 使用方法

### 运行程序
```bash
python main.py
```

### 测试模块
```bash
python test_modules.py
```

## 使用流程

1. **首次使用**: 输入孩子年龄和性别信息
2. **选择模式**: 单元剧或连续剧
3. **选择场景**: 从6种场景中选择
4. **自定义角色**: 输入主角类型和名字
5. **设置元素**: 输入故事主题元素
6. **选择概要**: 从AI生成的3个概要中选择
7. **生成故事**: 等待AI生成完整故事
8. **语音转换**: 可选择转换为语音文件

## 年龄适配规则

- **0-3岁**: 2岁难度，400-600字，简单词汇和重复句式
- **3-5岁**: 4岁难度，600-1000字，基础情节和角色互动
- **5岁以上**: 6岁难度，1000-1500字，复杂情节和情感表达

## 连续剧功能

- **28章结构**: 完整的长篇故事
- **智能续写**: 支持断点续写
- **进度保存**: 自动保存章节进度
- **场景匹配**: 相同场景可继续已有故事

## 文件说明

- `child_info.json`: 孩子信息记录
- `serial_story.json`: 连续剧进度记录
- `story_*.mp3`: 生成的语音文件

## 技术栈

- **AI服务**: Azure OpenAI GPT
- **语音合成**: Microsoft Edge TTS
- **配置管理**: python-dotenv
- **异步处理**: asyncio

## 开发说明

### 模块化设计
项目采用模块化设计，每个功能模块独立，便于维护和扩展：

- **解耦合**: 各模块功能独立，降低耦合度
- **可扩展**: 易于添加新功能模块
- **可测试**: 每个模块可独立测试
- **可复用**: 模块功能可在其他项目中复用

### 代码规范
- 使用类型提示
- 详细的函数文档
- 统一的错误处理
- 清晰的变量命名

## 故障排除

### 常见问题

1. **API连接失败**
   - 检查网络连接
   - 验证API密钥和端点配置
   - 确认Azure OpenAI服务状态

2. **语音合成失败**
   - 检查edge-tts安装
   - 验证网络连接
   - 确认文本内容格式

3. **文件保存失败**
   - 检查文件权限
   - 确认磁盘空间
   - 验证文件路径

### 调试模式
运行测试脚本验证各模块功能：
```bash
python test_modules.py
```

## 更新日志

### v2.0.0 (当前版本)
- ✅ 完成模块化重构
- ✅ 优化代码结构
- ✅ 增强错误处理
- ✅ 改进用户体验

### v1.0.0
- ✅ 基础故事生成功能
- ✅ 连续剧支持
- ✅ 语音合成功能

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。 