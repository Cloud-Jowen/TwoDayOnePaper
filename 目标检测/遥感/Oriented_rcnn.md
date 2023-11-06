# Oriented R-CNN for Object Detection

[**网络总结**](#网络总结)  
[**0.摘要 Abstract**](#0.摘要Abstract)  
[**1.介绍 Introduction**](#1.介绍Introduction)  
[**2.相关工作 Related work**](#2.相关工作Relatedwork)  
[**3.网络结构**](#3.网络结构)  
[**4.实验 Experiments**](#4.实验Experiments)  
[**5.结论 Conclusion**](#5.结论Conclusion)  



## 网络总结
参考博文链接：  
参考视频链接：  
源码链接：  
论文链接：  https://arxiv.org/pdf/2108.05699.pdf

<a id="0.摘要Abstract"></a>
## 0.摘要 Abstract
目前最先进的两阶段检测器通过耗时的方案生成定向提议，这减缓了检测器的速度，从而成为先进的定向物体检测系统中的计算瓶颈。本文提出了一个有效和简单的定向物体检测框架，称为定向R-CNN，它是一种具有良好准确性和高效性的通用两阶段定向检测器。具体而言，在第一阶段中，我们提出了一个定向区域建议网络（定向RPN），以近乎成本为零的方式直接生成高质量的定向提议。第二阶段是用于细化定向感兴趣区域（定向RoIs）并识别它们的定向R-CNN头。没有技巧的情况下，使用ResNet50的定向R-CNN在两个常用的定向物体检测数据集（包括DOTA（75.87％ mAP）和HRSC2016（96.50％ mAP））上实现了最先进的检测精度，在单个RTX 2080Ti上在图像大小为1024×1024的情况下的速度为15.1 FPS。我们希望我们的工作能够启发重新思考定向检测器的设计，并作为定向物体检测的基线。代码可在https://github.com/jbwang1997/OBBDetection上找到。

<a id="1.介绍Introduction"></a>
## 1.介绍 Introduction


<a id="2.相关工作Relatedwork"></a>
## 2.相关工作 Related work


<a id="3.网络结构"></a>
## 3.网络结构


<a id="4.实验Experiments"></a>
## 4.实验 Experiments

<a id="5.结论Conclusion"></a>
## 5.结论 Conclusion











