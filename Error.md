## 1. cv2 has no attribute 'gapi_wip_gst_GStreamerPipeline'
❌AttributeError: partially initialized module 'cv2' has no attribute 'gapi_wip_gst_GStreamerPipeline' (most likely due to a circular import)

✅解决办法：pip install opencv-python install "opencv-python-headless<4.3“

参考链接：https://blog.csdn.net/yuan2019035055/article/details/128076070

