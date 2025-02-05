# Pydantic 功能简介与代码示例

## 简介

Pydantic 是一个用于数据验证和设置管理的 Python 库，主要基于 Python 类型注解。它可以帮助开发者轻松地定义数据模型，并自动进行数据验证、序列化和文档生成。Pydantic 特别适用于处理来自外部源（如 API 请求、配置文件等）的数据，确保数据的完整性和一致性。

### 主要功能

1. **数据验证**：Pydantic 可以根据定义的数据模型自动验证输入数据，确保数据符合预期的类型和格式。
2. **数据转换**：Pydantic 可以自动将输入数据转换为定义的数据类型，例如将字符串转换为整数或日期。
3. **序列化与反序列化**：Pydantic 支持将数据模型实例转换为 JSON 或其他格式，并支持从这些格式反序列化为数据模型实例。
4. **文档生成**：Pydantic 可以自动生成数据模型的文档，方便开发者理解和使用。
5. **配置管理**：Pydantic 可以用于管理应用程序的配置，确保配置项的类型和值符合预期。

## 代码示例

以下是一个简单的 Pydantic 数据模型定义和使用示例。

### 安装 Pydantic

```bash
pip install pydantic
```

### 基本用法

**定义模型**

这里是一个简单的示例，展示如何定义一个数据模型User 

该模型拥有三个值:id/name/email,格式分别是int/str/str

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: str

# 创建一个 User 实例
user = User(id=1, name="Alice", email="alice@example.com")
print(user)
```

**数据验证**

Pydantic 会自动验证输入数据类型，如果传入的数据不符合预期，会引发 ValidationError：

```python
try:
    user = User(id="not_an_int", name="Bob", email="bob@example.com")
except ValidationError as e:
    print(e.json())  # 输出验证错误信息
```

**数据解析**

Pydantic 允许从 JSON 字符串或字典数据来实例化一个BaseModel：
```python
import json

# 从字典解析
data = {"id": 2, "name": "Charlie", "email": "charlie@example.com"}
user_from_dict = User(**data)
print(user_from_dict)

# 从 JSON 字符串解析
data_json = json.dumps(data)
user_from_json = User.parse_raw(data_json)
print(user_from_json)
```

⚠️ 上述示例中，通过字典实例化一个Basemodel对象,传入的值不是 `data` 而是 `**data`，这是因为传入`**data`时，是将字典 data 中的键值对作为参数进行传入，而不是data本身。如果传入的是data(以普通字典的形式传入)，那么在函数内部需要显式的访问字典的键来获取对应的值（value = data['key']）。用 `**data` 就可以自动遍历所有键值对，不用手动指定键名。非常 🌟Pythonic🌟

**Field**
