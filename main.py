import requests
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# آدرس API بایننس برای تست
binance_url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'

# لیست URL های پروکسی رایگان (۷ سرویس معروف) و نام سرویس‌ها
proxy_services = {
    'Proxy List Download': 'https://www.proxy-list.download/api/v1/get?type=https',
    'Proxy Scan': 'https://www.proxyscan.io/api/proxy?type=https',
    'Free Proxy List': 'https://www.free-proxy-list.net/',
    'Spys.one': 'http://spys.one/proxy.txt',
    'US Proxy': 'https://www.us-proxy.org/',
    'Socks Proxy': 'https://www.socks-proxy.net/',
    'Geonode': 'https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc&protocols=https'
}

# تابع برای دریافت پروکسی‌ها از سرویس‌های مختلف
def get_proxy_list():
    proxies = []
    for service_name, url in proxy_services.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                for proxy in response.text.splitlines():
                    proxies.append((service_name, proxy))  # ذخیره پروکسی به همراه نام سرویس
        except Exception as e:
            print(f"Error retrieving proxy list from {service_name} ({url}): {e}")
    return proxies

# تابع برای تست پروکسی با بایننس
def test_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(binance_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

# تابع برای ارسال ایمیل
def send_email(working_proxies, no_proxies=False):
    sender_email = os.getenv('EMAIL_USER')  # ایمیل فرستنده از secrets
    receiver_email = os.getenv('EMAIL_RECEIVER')  # ایمیل گیرنده از secrets
    password = os.getenv('EMAIL_PASSWORD')  # پسورد ایمیل فرستنده از secrets

    # تنظیمات ایمیل
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Proxy Checker Results'

    if no_proxies:
        body = "No working proxies were found."
    else:
        body = "Working proxies:\n\n"
        for service_name, proxy in working_proxies:
            body += f"{proxy} (from {service_name})\n"

    message.attach(MIMEText(body, 'plain'))

    # ارسال ایمیل با SSL و پورت 465
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # استفاده از SMTP_SSL و پورت 465
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# اجرای برنامه
proxy_list = get_proxy_list()
working_proxies = [(service_name, proxy) for service_name, proxy in proxy_list if test_proxy(proxy)]

# اگر پروکسی‌های سالم پیدا شدند، ایمیل ارسال می‌شود
if working_proxies:
    send_email(working_proxies)
else:
    send_email(working_proxies, no_proxies=True)  # ارسال ایمیل وقتی پروکسی کار نکرد
