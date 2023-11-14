# 操作
### 操作1 切分 DOTA 数据集
DOTA 数据集的图像尺寸过大，需要对其进行切分，通常切分至 1024 * 1024 大小的图片。同时，为了避免误切 gt，会在切分时保留一些重复区域 gap，通常 gap = 200  
更多切分细节请参考各论文中的实验设置。

**切分准备**  
进入 `./mmrotate/tools/data/dota/split/split_configs` 文件夹下，可以看到有如下几个 json 文件,需修改其内部的配置  
![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/05c659b0-04a1-4c0c-a64b-5b732b6d491b)  
`ms` \ `ss` 表示多尺度\单尺度切分，后缀表示相应的数据集  
以 `ss_train.sh` 为例，需要修改的一共有四个路径：`img_dirs`,`ann_dirs`,`save_dir`,`save_ext`。分别是 数据集图片文件夹\数据集标签文件夹\切分后的保存文件夹\切分后图片的后缀格式
例如：
```
  "img_dirs": [
    "/Jowen/dataset/DOTA/train/images"
  ],
  "ann_dirs": [
    "/Jowen/dataset/DOTA/train/labelTxt"
  ],
  "save_dir": "Jowen/dataset/DOTA-split-1024/train",
  "save_ext": ".png"
```
**请注意**：不要使用已经存在的文件夹作为`save_dir`，否则会报错

**切分命令**  
`python {root}/mmrotate/tools/data/dota/split/img_split.py --base-json {json_path}`
其中`{root}`和`{json_path}`请换成相应的路径，例如
```
python /Jowen/mmrotate/tools/data/dota/split/img_split.py --base-json Jowen/mmrotate/tools/data/dota/split/split_configs/ss_train.json
```

使用 `du -h {file}` 可以查看文件夹大小，切分后的数据集大小为
```
43M     /Jowen/dataset/DOTA-split-1024/train/annfiles
21G     /Jowen/dataset/DOTA-split-1024/train/images

536K    /Jowen/dataset/DOTA-split-1024/test/annfiles
14G     /Jowen/dataset/DOTA-split-1024/test/images

14M     /Jowen/dataset/DOTA-split-1024/val/annfiles
6.8G    /Jowen/dataset/DOTA-split-1024/val/images

42G     /Jowen/dataset/DOTA-split-1024
```



# 问题
### 问题1 对 DOTA 测试集进行测试时，计算 mAP 出现问题
**训练命令**   
**报错提示**  
**报错原因**    
**解决办法**    


