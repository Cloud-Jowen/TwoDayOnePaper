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

### 示例

```python
from datetime import datetime

from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int  
    name: str = 'John Doe'  
    signup_ts: datetime | None  
    tastes: dict[str, PositiveInt]  


external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',  
    'tastes': {
        'wine': 9,
        b'cheese': 7,  
        'cabbage': '1',  
    },
}

user = User(**external_data)  

print(user.id)  
#> 123
print(user.model_dump())  
"""
{
    'id': 123,
    'name': 'John Doe',
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
}
"""
```

