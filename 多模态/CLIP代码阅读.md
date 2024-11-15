
1. dataclass  

dataclass 是一个装饰器，用于装饰那些目的是存储数据的类(例如各种数据增强的概率等,open-clip中用dataclass来加载图像预处理的配置信息)。dataclass 可以有效减少样板代码，使得类的定义更加简洁和可读。

示例代码
```python
from dataclasses import dataclass
@dataclass
class PreprocessCfg: # clip 图像预处理的配置信息
    size: Union[int, Tuple[int, int]] = 224
    mode: str = 'RGB'
    mean: Tuple[float, ...] = OPENAI_DATASET_MEAN
    std: Tuple[float, ...] = OPENAI_DATASET_STD
    interpolation: str = 'bicubic'
    resize_mode: str = 'shortest'
    fill_color: int = 0

    def __post_init__(self):
        assert self.mode in ('RGB',)

    @property
    def num_channels(self):
        return 3

    @property
    def input_size(self):
        return (self.num_channels,) + to_2tuple(self.size)

```
在上述的 PreprocessCfg 内，定义了多个配置项，例如图片尺寸size，颜色通道，归一化均值和方差等。

不同于常见的类，PreprocessCfg 并没有 `__init__` 函数，这正是 `dataclass` 的方便之处，它可以自动生成包括但不限于 `__init__`、`__repr__`、`__eq__` 等方法，省去了大量的重复工作.

下面的示例给出了一个简单的 `dataclass` 示例，用来展示它的自动生成功能:

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    quantity: int

# 自动生成的构造函数 (__init__)
product = Product(name="Laptop", price=1200.00, quantity=5)

# 自动生成的字符串表示方法 (__repr__)
print(product)  # 输出: Product(name='Laptop', price=1200.0, quantity=5)

# 自动生成的比较方法 (__eq__)
another_product = Product(name="Laptop", price=1200.00, quantity=5)
print(product == another_product)  # 输出: True
```

贴一个上述 PreprogressCfg 的普通实例化方法，二者的对比可以更好的展示 `dataclass` 的便捷
```python
class PreprocessCfg:
    def __init__(self, size=224, mode='RGB', mean=None, std=None, interpolation='bicubic', resize_mode='shortest', fill_color=0):
        if mean is None:
            mean = OPENAI_DATASET_MEAN
        if std is None:
            std = OPENAI_DATASET_STD
        self.size = size
        self.mode = mode
        self.mean = mean
        self.std = std
        self.interpolation = interpolation
        self.resize_mode = resize_mode
        self.fill_color = fill_color
```

