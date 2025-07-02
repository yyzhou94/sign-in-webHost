# WebHostMost 自动化批量保号，每月1号自动登录一次面板，并且发送消息到Telegram

**WebHostMost 保活脚本**旨在自动登录 WebHostMost 客户区，定期检查账户的剩余时间，并通过 Telegram 机器人发送通知，提醒账户的保活状态和剩余时间。

此脚本可自动化保活操作，帮助您避免账户被删除，并且提供清晰的通知，确保您及时处理。

---

## 📦 项目结构

```
.
├── .github/
│   └── workflows/
│       └── webhostmost-keepalive.yml  # GitHub Actions 工作流配置
├── keepalive.py                      # 保活脚本，处理登录与通知
├── README.md                         # 本文档
└── requirements.txt                  # Python 依赖项
```

---

## 🛠️ 安装与配置

### 1. 克隆项目
#### 1.1 Fork 仓库

1. **访问原始仓库页面**：
    - 打开你想要 fork 的 GitHub 仓库页面。

2. **Fork 仓库**：
    - 点击页面右上角的 "Fork" 按钮，将仓库 fork 到你的 GitHub 账户下。
#### 1.2 Git 仓库
首先，将项目克隆到您的本地或服务器：

```bash
git clone https://github.com/your-username/webhostmost-keepalive.git
cd webhostmost-keepalive
```

### 2. 配置 GitHub Secrets

请在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中，添加以下 Secrets：
  - 转到你 fork 的仓库页面。
  - 点击 `Settings`，然后在左侧菜单中选择 `Secrets`。
  - 添加以下 Secrets：
  - `WEBHOST`: 账号信息,格式 账号1:密码 账号2:密码 账号3:密码
  - `TELEGRAM_BOT_TOKEN`: 你的 Telegram Bot 的 API Token。
  - `TELEGRAM_CHAT_ID`: 你的 Telegram Chat ID。

  - **获取方法**：
    - 在 Telegram 中创建 Bot，并获取 API Token 和 Chat ID。
    - 在 GitHub 仓库的 Secrets 页面添加这些值，确保它们安全且不被泄露。

### 3. 配置 GitHub Actions

#### 3.1 配置自动化工作流
  - 在你的 fork 仓库中，进入 `Actions` 页面。
  - 如果 Actions 没有自动启用，点击 `Enable GitHub Actions` 按钮以激活它。
  - 此脚本依赖于 GitHub Actions 定时执行。您可以在 `.github/workflows/webhostmost-keepalive.yml` 文件中设置定时任务。
  - 该工作流默认每月 **1号** 执行一次。如果您想更改执行频率，可以修改 `cron` 表达式。例如：
    
    ```yaml
    on:
      schedule:
        - cron: '0 0 1 * *'  # 每月 1号 执行一次（UTC时间）
    ```
    
#### 3.2 运行工作流
  - GitHub Actions 将会根据你设置的定时任务（例如每三天一次）自动运行脚本。
  - 如果需要手动触发，可以在 Actions 页面手动运行工作流。



---

## 🧰 使用方法

### 1. 定时运行脚本

GitHub Actions 将根据预设的时间表定期运行 `keepalive.py` 脚本。每次运行时，脚本会：

* 模拟登录 WebHostMost。
* 获取账户剩余时间信息。
* 将登录状态与剩余时间通过 Telegram 发送给您。

### 2. 查看 Telegram 通知

每次运行结束后，Telegram 机器人将发送一条通知，告知您每个账户的保活状态和剩余时间。

示例通知内容：

```
📡 WEBHOST登录状态:

🟢 user1@example.com 登录成功 ✅
⏱️ 剩余时间：44 天
🟢 user1@example.com 登录成功 ✅
⏱️ 剩余时间：44 天

🔴 user2@example.com 登录失败 ❌: 未能跳转到仪表板页面
```

---

## ⚠️ 注意事项

* **安全性**：确保 GitHub Secrets 中的邮箱、密码、Telegram Token 等信息的保密性，不要直接暴露在代码中。
* **执行频率**：通过 GitHub Actions 的 `cron` 表达式，您可以设置脚本执行的频率（如每天、每周等）。
* **Telegram 配置**：确保 Telegram Bot 已成功配置并能发送消息到指定的 Chat ID。
* **兼容性**：此脚本目前仅支持 WebHostMost 客户区。

---

## 📬 支持与贡献

![edgeone](https://edgeone.ai/media/34fe3a45-492d-4ea4-ae5d-ea1087ca7b4b.png)

如果您遇到任何问题，欢迎通过 Issues 提交反馈或改进建议。

如果您希望贡献代码，欢迎提交 Pull Request，我们会尽快审核并合并您的更改。

---

## 🎯 许可证

本项目采用 [MIT 许可证](LICENSE)，详情请见 [LICENSE 文件](LICENSE)。

---

### 💡 免责声明

本项目是为 WebHostMost 用户提供的自动化保活工具，仅限个人使用。使用本脚本时，请确保您遵守 WebHostMost 的服务条款及相关法律法规。此脚本的作者不对因使用该脚本而产生的任何问题或损失负责。

---
