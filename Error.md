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

✅提示：请严格按照官网教程进行安装，出现 _C 问题请检查安装步骤

❌OSError: We couldn't connect to 'https://huggingface.co' to load this file, couldn't find it in the cached files and it looks like bert-base-uncased is not the path to a directory containing a file named config.json.

✅解决办法：去 huggingface 上下载对应的 tokenizer 权重 https://huggingface.co/google-bert/bert-base-chinese  
把上述链接的权重全部下载好  
替换 ./GroundingDINO/groundingdino/util/inference.py 的 line80 为  

```python
from transformers import AutoTokenizer, AutoModelForMaskedLM # 在开头添加
tokenizer = AutoTokenizer.from_pretrained("./GroundingDINO/bert-base-chinese")
```

并替换 './GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py' 的 line 34  
```python
text_encoder_type = "./GroundingDINO/bert-base-chinese"
```


❌RuntimeError: Error(s) in loading state_dict for GroundingDINO:
        size mismatch for bert.embeddings.word_embeddings.weight: copying a param with shape torch.Size([30522, 768]) from checkpoint, the shape in current model is torch.Size([21128, 768]).

✅解决办法： 修改 ./GroundingDINO/groundingdino/util/get_tokenlizer.py 的 line 25 为  
```python
return BertModel.from_pretrained(text_encoder_type,ignore_mismatched_sizes=True)
```  

修改 ./GroundingDINO/bert-base-chinese/config.json 的 line 24 为  
```python
"vocab_size": 30522 ,
```


