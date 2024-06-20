### README 文件

#### 项目简介

本项目展示了如何使用自然语言命令管理服务器，利用 OpenAI 的 GPT 模型和 Paramiko 库进行 SSH 连接。

#### 需求

- Python 3.7+
- OpenAI API 密钥
- Paramiko 库

#### 设置步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/wuxuebing-1/naturalLanguageServerManagement.git
   cd natural-language-server-management
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 在 `config.py` 中配置你的 OpenAI API 密钥和服务器信息。

#### 使用方法

运行主脚本：
```bash
python main.py
```

输入自然语言命令以管理服务器。

#### 许可证

[MIT License](LICENSE)
