
1. dataclass
dataclass 是一个装饰器，用于装饰那些目的是存储数据的类。dataclass 可以有效减少样板代码，使得类的定义更加简洁和可读。
示例代码
```python
class PreprocessCfg: # clip 图像预处理的配置信息
    size: Union[int, Tuple[int, int]] = 224
    mode: str = 'RGB'
    mean: Tuple[float, ...] = OPENAI_DATASET_MEAN # (0.48145466, 0.4578275, 0.40821073)
    std: Tuple[float, ...] = OPENAI_DATASET_STD   # (0.26862954, 0.26130258, 0.27577711)
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

