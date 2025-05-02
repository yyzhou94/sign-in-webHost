from playwright.sync_api import sync_playwright
import os
import requests
from bs4 import BeautifulSoup

def send_telegram_message(message):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

def login_koyeb(email, password):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        # 访问登录页面
        page.goto("https://client.webhostmost.com/login")

        # 输入邮箱和密码
        page.get_by_placeholder("Enter email").click()
        page.get_by_placeholder("Enter email").fill(email)
        page.get_by_placeholder("Password").click()
        page.get_by_placeholder("Password").fill(password)
    
        # 点击登录按钮
        page.get_by_role("button", name="Login").click()

        # 等待可能出现的错误消息或成功登录后的页面        
        try:
            # 等待可能的错误消息
            error_message = page.wait_for_selector('.MuiAlert-message', timeout=5000)
            if error_message:
                error_text = error_message.inner_text()
                return f"账号 {email} 登录失败: {error_text}"
        except:
            # 如果没有找到错误消息,检查是否已经跳转到仪表板页面
            try:
                page.wait_for_url("https://client.webhostmost.com/clientarea.php", timeout=5000)

                #aa#############################
                message = ''
                try:
                    days = page.locator('#timer-days').inner_text()
                    message = (f"\n⏳ 剩余时间：{days} 天")
                except Exception as e:
                    message = f"但无法解析剩余时间：{e}"
                #aa###################################

                return f"🟢 {email} 登录成功 ✅{message}\n"
            except:
                return f"账号 {email} 登录失败: 未能跳转到仪表板页面"
                
        finally:
            browser.close()

if __name__ == "__main__":
    accounts = os.environ.get('WEBHOST', '').split()
    login_statuses = []

    for account in accounts:
        email, password = account.split(':')
        status = login_koyeb(email, password)
        login_statuses.append(status)
        print(status)

    if login_statuses:
        message = "WEBHOST登录状态:\n\n" + "\n".join(login_statuses)
        result = send_telegram_message(message)
        print("消息已发送到Telegram:", result)
    else:
        error_message = "没有配置任何账号"
        send_telegram_message(error_message)
        print(error_message)
