# Pydantic 功能简介与代码示例

  - [简介](#简介)
    - [主要功能](#主要功能)
  - [代码示例](#代码示例)
    - [安装 Pydantic](#安装-pydantic)
    - [基本用法](#基本用法)

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
# id=1 name='Alice' email='alice@example.com'
```

**数据验证**

Pydantic 会自动验证输入数据类型，如果传入的数据不符合预期，会引发 ValidationError：

```python
try:
    user = User(id="not_an_int", name="Bob", email="bob@example.com")
except ValidationError as e:
    print(e.json())  # 输出验证错误信息
# [{"type":"int_parsing","loc":["id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"not_an_int","url":"https://errors.pydantic.dev/2.10/v/int_parsing"}]
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

### Field

`Field` 是 Pydantic 提供的一个函数，用于为模型的字段添加额外的元数据和验证规则。通过 `Field`，你可以更精细地控制字段的行为，例如：

- **添加字段的描述**：用于文档生成。
- **设置默认值**：提供字段的默认值。
- **添加验证规则**：如最小值、最大值、正则表达式等。
- **标记字段是否必需**：指示某个字段在实例化时是否是必填项。

**示例**

以下是一个使用 `Field` 的简单示例：

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="用户的唯一标识符") # Field 里的 ... 表示该字段是必须的,在创建模型实例时必须提供值
    username: str = Field(
        ..., 
        min_length=3,  # 字符串的最小长度
        max_length=50, # 字符串的最大长度
        description="用户名，长度必须在 3 到 50 个字符之间"
    )
    age: int = Field(
        default=18, 
        ge=0,   # greater than or equal to 大于等于
        le=120, # less than or equal to 小于等于
        description="用户的年龄，必须在 0 到 120 之间"
    )
    email: str = Field(
        ..., 
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", # regular expression 正则表达式
        description="用户的电子邮件地址"
    )
```
输出
```python
id=1 username='john_doe' age=18 email='john.doe@example.com'
{
  "title": "User",
  "type": "object",
  "properties": {
    "id": {
      "description": "用户的唯一标识符",
      "example": 1,
      "type": "integer"
    },
    "username": {
      "description": "用户名，长度必须在 3 到 50 个字符之间",
      "example": "john_doe",
      "minLength": 3,
      "maxLength": 50,
      "type": "string"
    },
    "age": {
      "description": "用户的年龄，必须在 0 到 120 之间",
      "example": 25,
      "default": 18,
      "minimum": 0,
      "maximum": 120,
      "type": "integer"
    },
    "email": {
      "description": "用户的电子邮件地址",
      "example": "john.doe@example.com",
      "pattern": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
      "type": "string"
    }
  },
  "required": [
    "id",
    "username",
    "email"
  ]
}
```
