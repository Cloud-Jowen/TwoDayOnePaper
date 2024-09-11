# FaceNet: A Unified Embedding for Face Recognition and Clustering

[**相关链接**](#相关链接)  
[**0.摘要 Abstract**](#0.摘要Abstract)  
[**1.介绍 Introduction**](#1.介绍Introduction)  
[**2.相关工作 Related work**](#2.相关工作Relatedwork)  
[**3.网络结构**](#3.网络结构)  
&emsp;[**3.1**](#3.1)  
[**4.实验 Experiments**](#4.实验Experiments)  
[**5.结论 Conclusion**](#5.结论Conclusion)  



## 相关链接
参考博文链接：  
参考视频链接：  
源码链接：  
论文链接：   https://arxiv.org/pdf/1503.03832  

<a id="0.摘要Abstract"></a>
## 0.摘要 Abstract
尽管在面部识别领域取得了显著的近期进展（[10，14，15，17]），但大规模实施有效的面部验证和识别仍对当前方法构成严重挑战。本文提出了一种系统，称为FaceNet，该系统直接学习从面部图像到紧凑的欧几里得空间的映射，在此空间中距离直接对应于面部相似度的一种度量。一旦生成了这个空间，使用标准技术就可以轻松地将FaceNet嵌入作为特征向量来实现面部识别、验证和聚类等任务。 

我们的方法使用一个训练有素的深度卷积网络，直接优化嵌入本身，而不是像以前的深度学习方法那样使用中间瓶颈层。为了训练，我们使用了一个新颖的在线三元组挖掘方法生成的粗略对齐匹配/非匹配人脸块的三元组。我们的方法的优势在于更高的表示效率：我们仅用每张脸128字节就达到了最先进的面部识别性能。 

在广泛使用的Labeled Faces in the Wild (LFW) 数据集上，我们的系统达到了新的记录精度为99.63%，在YouTube Faces DB中达到95.12%。与最佳发表结果相比，在两个数据集上，我们的系统将错误率降低了30%。 

我们还引入了和谐嵌入的概念，以及和谐三元组损失函数，这些描述了由不同网络生成的、可以互相兼容并直接比较的不同版本的人脸嵌入。 
     
<a id="1.介绍Introduction"></a>
## 1.介绍 Introduction


<a id="2.相关工作Relatedwork"></a>
## 2.相关工作 Related work


<a id="3.网络结构"></a>
## 3.网络结构

<a id="3.1"></a>
### 3.1


<a id="4.实验Experiments"></a>
## 4.实验 Experiments

<a id="5.结论Conclusion"></a>
## 5.结论 Conclusion










