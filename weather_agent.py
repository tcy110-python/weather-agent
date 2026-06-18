#!/usr/bin/env python3
"""
🌀 极简天气智能体 — 直接复制就能跑
用法: python weather_agent.py
"""

import requests
import sys

# ============ ⚠️ 把这里换成你自己的 API Key ============
API_KEY = "81cbea78948eb21df127f16f351e1abd"
# =========================================================

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict | None:
    """调 API 获取天气原始数据"""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",   # 摄氏度
        "lang": "zh_cn"       # 中文描述
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        data = resp.json()
        if data.get("cod") != 200:
            print(f"❌ 错误: {data.get('message', '未知错误')}（city={city}）")
            return None
        return data
    except Exception as e:
        print(f"❌ 网络请求失败: {e}")
        return None


def format_report(data: dict) -> str:
    """把 JSON 数据整理成人话"""
    city     = data["name"]
    country  = data["sys"]["country"]
    temp     = data["main"]["temp"]
    feels    = data["main"]["feels_like"]
    desc     = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind     = data["wind"]["speed"]

    return f"""
🌍 {city}, {country}
━━━━━━━━━━━━━━━━━━━━━━
🌤  天气：{desc}
🌡  当前温度：{temp}°C（体感 {feels}°C）
💧 湿度：{humidity}%
🌬  风速：{wind} m/s
━━━━━━━━━━━━━━━━━━━━━━
"""


def chat_mode():
    """交互聊天模式——像跟一个小智能体对话"""
    print("🤖 天气智能体已启动！输入城市名查询，输入 exit / quit 退出\n")
    while True:
        city = input("🗣 你说：").strip()
        if city.lower() in ("exit", "quit", ""):
            print("👋 再见！")
            break
        data = get_weather(city)
        if data:
            print(format_report(data))


if __name__ == "__main__":
    if API_KEY.startswith("把你") or len(API_KEY) < 10:
        print("\n⚠️  请先去第 13 行把 API_KEY 换成你自己的！")
        print("   获取地址: https://openweathermap.org/api\n")
        sys.exit(1)

    # 如果运行时带了参数，就查一次退出；否则进入聊天模式
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
        data = get_weather(city)
        if data:
            print(format_report(data))
    else:
        chat_mode()
