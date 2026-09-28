import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('DEEPSEEK_BASE_URL', "https://api.deepseek.com")
)

messages = []

while True:
    user_input = input("输入你的问题: ")

    # 推出循环
    if user_input.strip().lower() in ("quit", "exit", "q"):
        print("再见！")
        break

    # 发送用户消息
    messages.append({"role": "user", "content": user_input})

    # 接收AI回复
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    # 输出AI回复
    reply = response.choices[0].message
    messages.append(reply)
    print(f"AI: {reply.content}\n")
