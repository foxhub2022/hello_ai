# Python dict（字典）增删改查与迭代

Python 的 `dict`（字典）是键值对结构，下面是常用的增删改查和迭代操作。

## 创建

```python
# 空字典
d = {}
d = dict()

# 带初始数据
d = {"name": "Alice", "age": 18}
d = dict(name="Alice", age=18)
```

## 增 / 改

```python
d["city"] = "Beijing"   # 键不存在 → 新增
d["age"] = 20           # 键已存在 → 修改（覆盖）

# 批量更新（存在的覆盖，不存在的新增）
d.update({"age": 21, "job": "dev"})

# setdefault：键存在就返回原值，不存在才写入
d.setdefault("hobby", "reading")
```

## 查

```python
d["name"]               # 键不存在会抛 KeyError
d.get("name")           # 推荐：不存在返回 None
d.get("xxx", "默认值")   # 不存在时返回默认值

"name" in d             # 判断键是否存在 → True/False
len(d)                  # 键值对数量
d.keys()                # 所有键
d.values()              # 所有值
d.items()               # 所有 (键, 值) 对
```

## 删

```python
del d["age"]                    # 按键删除，键不存在抛 KeyError
d.pop("city")                   # 删除并返回该值
d.pop("xxx", "默认值")           # 键不存在时返回默认值，不报错
d.popitem()                     # 删除并返回最后插入的一对 (Python 3.7+)
d.clear()                       # 清空整个字典
```

## 迭代

```python
# 只遍历键
for key in d:
    print(key)

for key in d.keys():
    print(key)

# 只遍历值
for value in d.values():
    print(value)

# 同时遍历键和值（最常用）
for key, value in d.items():
    print(key, value)

# 遍历时想修改字典：先复制一份，避免报错
for key in list(d.keys()):
    if key == "age":
        del d[key]
```

## 几个实用技巧

```python
# 字典推导式
squares = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 字典合并（Python 3.9+）
merged = d1 | d2          # 合并，d2 覆盖同名键
d |= {"extra": 1}         # 原地合并

# 计数场景：统计每个元素出现次数
from collections import Counter
c = Counter(["a", "b", "a", "c", "a"])
# Counter({'a': 3, 'b': 1, 'c': 1})
```

## 核心记忆点

- 取值优先用 `.get()`，避免 `KeyError`
- 删除优先用 `.pop(key, 默认值)`
- 同时取键值用 `.items()`
- 遍历过程中不要直接增删字典，先 `list()` 复制键
