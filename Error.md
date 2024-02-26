## 1. cv2 has no attribute 'gapi_wip_gst_GStreamerPipeline'
❌AttributeError: partially initialized module 'cv2' has no attribute 'gapi_wip_gst_GStreamerPipeline' (most likely due to a circular import)

✅解决办法：pip install opencv-python install "opencv-python-headless<4.3"

参考链接：https://blog.csdn.net/yuan2019035055/article/details/128076070

## 2. cv2 相关 ImportError: libGL.so.1: cannot open shared object file: No such file or directory
❌ImportError: libGL.so.1: cannot open shared object file: No such file or directory

✅解决办法：pip install opencv-python install "opencv-python-headless<4.3"

参考链接：https://blog.csdn.net/qq_39691492/article/details/130688233

## 3. 'cv2' has no attribute '_registerMatType' (most likely due to a circular import)

❌AttributeError: partially initialized module 'cv2' has no attribute '_registerMatType' (most likely due to a circular import)

✅解决办法：pip install opencv-python install "opencv-python-headless<4.3"

参考链接：

## 4. GroundingDINO 的 tokenizer 

❌OSError: We couldn't connect to 'https://huggingface.co' to load this file, couldn't find it in the cached files and it looks like bert-base-uncased is not the path to a directory containing a file named config.json.

✅解决办法：去 huggingface 上下载对应的 tokenizer 权重 https://huggingface.co/google-bert/bert-base-chinese  
把上述链接的权重全部下载好  
替换 ./GroundingDINO/groundingdino/util/inference.py 的 line80 为  

```python 
tokenizer = AutoTokenizer.from_pretrained("./GroundingDINO/bert-base-chinese")
```

参考链接：
