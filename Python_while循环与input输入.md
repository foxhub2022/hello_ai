# Python 学习笔记：while 死循环与 input() 输入

> 配套示例文件：`serial_chat.py`（一个可以在终端里和 AI 连续对话的小程序）

---

## 一、while 死循环

### 1. 基本写法

```python
while True:
    # 循环体：这里的代码会无限重复执行
```

- `while` 后面跟一个条件，条件为真（True）就执行循环体
- `True` 是永远成立的条件，所以循环不会自己停止
- 循环体必须**缩进 4 个空格**（Python 靠缩进区分代码层级）

### 2. 如何退出：break

死循环必须在循环体内部用 `break` 主动退出，否则程序只能靠 `Ctrl + C` 强制终止。

```python
while True:
    command = input("请输入命令: ")
    if command == "quit":
        break          # 立刻跳出整个 while 循环
    print("你输入了:", command)

print("程序结束")
```

### 3. 其他常用控制关键字

| 关键字 | 作用 |
|--------|------|
| `break` | 立刻跳出整个循环 |
| `continue` | 跳过本轮剩余代码，直接进入下一轮 |
| `while 条件:` | 条件不满足时循环自然结束（不一定要写 True） |

`continue` 示例：

```python
while True:
    text = input("> ")
    if text == "":
        continue   # 空输入不做处理，直接回去重新等输入
    if text == "quit":
        break
    print("收到:", text)
```

---

## 二、input()：从键盘获取输入

### 1. 基本用法

```python
name = input("请输入你的名字: ")
```

执行过程：

1. 程序运行到 `input()` 时**暂停**，等待用户敲键盘
2. 用户输入内容后按**回车**
3. 回车之前的内容（不含回车符）作为**字符串**返回，赋值给变量

### 2. 重要特性：返回值永远是字符串

无论用户输入的是 `18` 还是 `3.14`，`input()` 拿到的都是字符串 `"18"`、`"3.14"`，不能直接做数学运算，必须先转换类型：

```python
age = int(input("年龄: "))        # str -> int（整数）
price = float(input("价格: "))    # str -> float（小数）

print(age + 1)                    # 转换后才能做加减运算
```

如果输入的内容无法转换（比如在要求数字时输入了字母），会抛出 `ValueError`，以后可以用 `try/except` 处理。

### 3. 常用输入处理技巧

```python
text = input("> ")

text.strip()          # 去掉首尾空格和换行
text.lower()          # 转成小写（判断 quit / QUIT / Quit 时很有用）
text == ""            # 判断用户是否直接按了回车（空输入）
```

---

## 三、实战：终端 AI 对话程序（serial_chat.py）

下面的程序把 while 循环和 input() 结合起来，实现了一个能**连续对话、保留上下文**的 AI 聊天工具：

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('DEEPSEEK_BASE_URL', "https://api.deepseek.com")
)

messages = []                          # ① 历史记录放在循环外面

while True:                            # ② 死循环：一直聊下去
    user_input = input("你: ")         # ③ 等待用户输入

    if user_input.strip().lower() in ("quit", "exit", "q"):
        print("再见！")
        break                          # ④ 输入退出命令，结束循环

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    reply = response.choices[0].message
    messages.append(reply)             # ⑤ 把 AI 回复也存进历史
    print(f"AI: {reply.content}\n")
```

### 关键点解析

1. **`messages = []` 必须放在 while 循环外面**
   列表用于累积全部对话历史，AI 每次调用都能看到之前说过的话。如果放进循环体里，每轮都会被清空，AI 就会"失忆"。

2. **退出命令的判断**
   `user_input.strip().lower()` 先去空格再转小写，所以 `quit`、` QUIT `、`Q` 都能正确退出，对用户更友好。

3. **打印内容要选对**
   `reply` 是一个消息对象，直接 `print(reply)` 会输出一大串结构信息；真正的回复文本在 `reply.content` 里。

### 运行方法

先在项目根目录的 `.env` 文件中配置好 API Key：

```text
DEEPSEEK_API_KEY=你的密钥
```

然后在 PowerShell 中运行（项目要求使用虚拟环境 `myenv`）：

```powershell
.\myenv\Scripts\python.exe serial_chat.py
```

输入 `quit` 并回车即可退出程序。

---

## 四、常见错误清单

| 错误写法 | 问题 | 正确写法 |
|----------|------|----------|
| `whiile :` | 单词拼错，且 while 后必须是条件 | `while True:` |
| 循环体没有缩进 | Python 靠缩进划分循环体，会报 `IndentationError` | 循环体统一缩进 4 空格 |
| 忘记写退出条件 | 程序只能靠 `Ctrl + C` 强制结束 | 在循环内用 `if ...: break` |
| `age = input(); age + 1` | input 返回字符串，字符串不能加整数 | `age = int(input())` |
| 把需要累积的变量定义在循环内 | 每轮循环变量被重置 | 累积型变量放在 `while` 之前 |

---

## 五、课后练习

1. 写一个程序，反复让用户输入数字，输入 `done` 时结束，并打印所有数字的总和与平均值。
2. 写一个猜数字游戏：程序内置一个答案，循环接收用户猜测，提示"大了/小了"，猜对后用 `break` 退出。
3. 给 `serial_chat.py` 增加功能：用户直接按回车（空输入）时不调用 API，提示"请输入内容"。
