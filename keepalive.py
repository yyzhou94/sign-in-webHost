import os
import requests
from bs4 import BeautifulSoup

emails = os.environ['WHM_EMAILS'].split(',')
passwords = os.environ['WHM_PASSWORDS'].split(',')

login_url = 'https://client.webhostmost.com/login'
dashboard_url = 'https://client.webhostmost.com/clientarea.php'

# Telegram 配置
telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded'
}

messages = []  # 最终要推送的消息内容

for email, password in zip(emails, passwords):
    with requests.Session() as session:
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})
        token = token_input['value'] if token_input else ''

        payload = {
            'username': email.strip(),
            'password': password.strip(),
            'token': token,
        }

        response = session.post(login_url, data=payload, headers=headers)

        if 'Logout' in response.text or 'logout' in response.text:
            dashboard_response = session.get(dashboard_url)
            soup = BeautifulSoup(dashboard_response.text, 'html.parser')

            try:
                days = soup.find('span', id='timer-days').text.strip()
                hours = soup.find('span', id='timer-hours').text.strip()
                minutes = soup.find('span', id='timer-minutes').text.strip()
                seconds = soup.find('span', id='timer-seconds').text.strip()

                message = (
                    f"🟢 <b>{email}</b> 登录成功 ✅\n"
                    f"⏳ <b>剩余时间：</b>\n"
                    f"🗓️ {days} 天\n"
                    f"⏰ {hours} 小时 {minutes} 分钟 {seconds} 秒"
                )
            except Exception as e:
                message = f"⚠️ <b>{email}</b> 登录成功，但无法解析剩余时间：{e}"
        else:
            message = f"🔴 <b>{email}</b> 登录失败 ❌，请检查邮箱或密码"

        messages.append(message)

# 整合并推送 Telegram 消息
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}"
    payload = {
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("❗Telegram 消息发送失败")
    else:
        print("📬 Telegram 消息已发送")

# 构造消息
full_message = "📡 <b>WebHostMost 保活报告</b>\n\n" + "\n\n".join(messages)
send_telegram_message(full_message)
