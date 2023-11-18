# Oriented R-CNN for Object Detection

[**相关链接**](#相关链接)  
[**0.摘要 Abstract**](#0.摘要Abstract)  
[**1.介绍 Introduction**](#1.介绍Introduction)  
[**2.相关工作 Related work**](#2.相关工作Relatedwork)  
[**3.网络结构**](#3.网络结构)  
&emsp;[**3.1 OrientedRPN**](#3.1OrientedRPN)  
&emsp;&emsp;[**3.1.1 中点偏移表示法**](#3.1.1中点偏移表示法MidpointOffsetRepresentation)  
&emsp;&emsp;[**3.1.2 损失函数**](#3.1.2损失函数LossFunction)  
&emsp;[**3.2 OrientedR-CNNHead**](#3.2OrientedR-CNNHead)  
&emsp;&emsp;[**3.2.1 RotatedRoIAlign**](#3.2.1RotatedRoIAlign)  
&emsp;[**3.3 实现细节**](#3.3实现细节ImplementationDetails)  
[**4.实验 Experiments**](#4.实验Experiments)  
&emsp;[**4.2 参数设置**](#4.2参数设置Parametersettings)  
&emsp;[**4.3 有向RPN的评估**](#4.3有向RPN的评估EvaluationofOrientedRPN)  
&emsp;[**4.4 和SOTA方法相比**](#4.4和SOTA方法相比ComparisonwithState-of-the-Arts)  
&emsp;[**4.5 速度与准确性**](#4.5速度与准确性SpeedversusAccuracy)  
[**5.结论 Conclusion**](#5.结论Conclusion)  



## 相关链接
参考博文链接：  
参考视频链接：  
源码链接：  https://github.com/jbwang1997/OBBDetection  
论文链接：  https://arxiv.org/pdf/2108.05699.pdf  

<a id="0.摘要Abstract"></a>
## 0.摘要 Abstract
目前最先进的两阶段检测器通过耗时的方案生成定向proposal，这减缓了检测器的速度，从而成为先进的定向物体检测系统中的计算瓶颈。本文提出了一个有效和简单的定向物体检测框架，称为定向R-CNN，它是一种具有良好准确性和高效性的通用两阶段定向检测器。具体而言，在第一阶段中，我们提出了一个定向区域proposal网络（定向RPN），以近乎成本为零的方式直接生成高质量的定向proposal。第二阶段是用于细化定向感兴趣区域（定向RoIs）并识别它们的定向R-CNN头。没有技巧的情况下，使用ResNet50的定向R-CNN在两个常用的定向物体检测数据集（包括DOTA（75.87％ mAP）和HRSC2016（96.50％ mAP））上实现了最先进的检测精度，在单个RTX 2080Ti上在图像大小为1024×1024的情况下的速度为15.1 FPS。我们希望我们的工作能够启发重新思考定向检测器的设计，并作为定向物体检测的基线。  
代码可在 https://github.com/jbwang1997/OBBDetection 上找到。

<a id="1.介绍Introduction"></a>
## 1.介绍 Introduction
大多数现有的最先进的定向物体检测方法[7, 37, 41]依赖于基于proposal的框架，如Fast/Faster R-CNN [11, 10, 32]。它们涉及两个关键步骤：(i) 生成定向proposal，(ii) 对proposal进行细化并将其分类到不同的类别中。然而，生成定向proposal的步骤在计算上是昂贵的。  

早期生成定向proposal的方法之一是旋转的区域proposal网络（简称为旋转RPN）[26]，它在每个位置放置了54个具有不同角度、尺度和长宽比的anchor，如图1(a)所示。引入旋转anchor提高了召回率，并在定向物体稀疏分布时表现良好。然而，大量的anchor导致了巨大的计算和内存占用。为了解决这个问题，RoI Transformer [7]通过复杂的过程从水平RoIs中学习定向proposal，该过程涉及RPN、RoI对齐和回归（见图1(b)）。RoI Transformer方案提供了有希望的定向proposal，并大幅减少了旋转anchor的数量，但也带来了昂贵的计算成本。现在，如何设计一个优雅而高效的解决方案来生成定向proposal是突破现有最先进的定向检测器计算瓶颈的关键。

为了进一步推动技术的发展，我们调查了为什么基于proposal的定向检测器的效率迄今为止还不够高。我们观察到，阻碍proposal驱动检测器速度的主要障碍来自proposal生成阶段。一个自然而直观的问题是：我们能否设计一个通用而简单的定向区域proposal网络（简称为定向RPN），直接生成高质量的定向proposal呢？在这个问题的推动下，本文提出了一种简单的双阶段定向物体检测框架，称为定向R-CNN，它在检测准确性方面达到了最先进的水平，同时与单阶段定向检测器在效率方面有着一定的竞争力。

具体而言，在定向R-CNN的第一阶段，我们提出了一个概念上简单的定向RPN（见图1(c)）。我们的定向RPN是一种轻量级的全卷积网络，其参数数量比旋转RPN和RoI Transformer+要少得多，从而降低了过拟合的风险。我们通过将RPN回归分支的输出参数数量从四个改变为六个来实现这一点。然而，没有免费的午餐。定向RPN的设计受益于我们提出的定向物体表示方案，称为中点偏移表示。对于图像中的任意定向物体，我们利用六个参数来表示它们。中点偏移表示继承了水平回归机制，并为预测定向proposal提供了有界约束。定向R-CNN的第二阶段是定向R-CNN检测头：通过旋转的RoI对齐提取每个定向proposal的特征，并进行分类和回归。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/d5808687-93cc-48c1-b3fb-59a555882299)  
(图1：不同生成有向proposal方案的比较。（a）旋转RPN密集地放置具有不同尺度、比例和角度的旋转anchor。（b）RoI Transformer+从水平RoI中学习有向proposal。它涉及到RPN、RoI对齐和回归。（c）我们提出的有向RPN以几乎零成本的方式生成高质量的proposal。有向RPN的参数数量约为RoI Transformer+的1/3000和旋转RPN的1/15。)

在没有华而不实的装饰下，我们在两个流行的定向物体检测基准数据集DOTA和HRSC2016上评估了我们的定向R-CNN方法。我们使用ResNet-50-FPN网络，在所有现有最先进的检测器中，达到了最高的准确性，DOTA数据集上达到了75.87%的mAP，HRSC2016数据集上达到了96.50%的mAP，同时在单个RTX 2080Ti上以1024×1024的图像尺寸运行时的帧率为15.1 FPS。因此，定向R-CNN在准确性和效率两方面都是一个实用的物体检测框架。我们希望我们的方法能够启发对定向物体检测器和定向物体回归方案设计的重新思考，并作为定向物体检测的稳定基准。关于未来的研究，我们的代码可在 https://github.com/jbwang1997/OBBDetection 上获取。

<a id="2.相关工作Relatedwork"></a>
## 2.相关工作 Related work
在过去的十年中，物体检测领域取得了显著进展[23, 33, 2, 42, 31, 24, 45, 13, 20, 29]。作为物体检测的一个延伸分支，定向物体检测 [7, 37, 26, 12, 5, 28]由于其广泛的应用而受到了广泛关注。  

依赖于水平边界框的通用物体检测方法（如Faster R-CNN）无法紧密地定位图像中的定向物体，因为水平边界框可能包含更多的背景区域或多个物体。这导致了最终分类置信度和定位准确性之间的不一致。为了解决这个问题，人们已经付出了很多努力。例如，夏等人 [36]构建了一个带有定向注释的大规模物体检测基准数据集，名为DOTA。许多现有的定向物体检测器 [7, 37, 41, 26, 25, 18]主要基于典型的基于proposal的物体检测框架。对于定向物体，一种自然的解决方案是设置旋转的anchor [26, 25]，例如旋转RPN [26]，其中不同角度、尺度和长宽比的anchor被放置在每个位置上。这些密集的旋转anchor导致了大量的计算和内存占用。  

为了减少旋转anchor的数量并降低特征与物体之间的不匹配，Ding等人[7]提出了RoI transformer方法，它从RPN生成的水平RoIs中学习旋转RoIs。这种方法极大地提高了定向物体检测的准确性。然而，这使得网络变得沉重和复杂，因为它涉及到全连接层和RoI对齐操作来学习旋转RoIs。为了解决小型、混乱、旋转物体检测的挑战，Yang等人[41]在Faster R-CNN的通用物体检测框架上建立了一种定向物体检测方法。Xu等人[37]提出了一种新的定向物体表示，称为滑动顶点。它通过在Faster R-CNN头部回归分支上学习四个顶点滑动偏移量来实现定向物体检测。然而，这两种方法仍然采用水平RoIs来执行分类和定向边界框回归，仍然存在严重的物体和特征之间的不对齐问题。  

此外，一些工作[12、28、39、27、43、16、40、47、15]探索了单阶段或无anchor的定向物体检测框架：输出物体类别和定向边界框，而不涉及区域proposal生成和RoI对齐操作。例如，Yang等人[39]提出了一种改进的单阶段定向物体检测器，包括特征改进和渐进回归两个关键改进，以解决特征不对齐问题。Ming等人[27]基于RetinaNet [22]设计了一种新的标签分配策略，用于单阶段定向物体检测。它通过新的匹配策略动态地分配正或负anchor。Han等人[12]提出了一种单镜头对齐网络(S2ANet)用于定向物体检测。S2ANet旨在通过深度特征对齐来缓解分类得分和位置精度之间的不一致性。Pan等人[28]基于无anchor物体检测方法CenterNet [46]设计了一个动态精炼网络(DRN)用于定向物体检测。  

与上述方法相比，我们的工作属于proposal型定向物体检测方法。它专注于设计一个高效的定向RPN，以打破生成定向proposal的计算瓶颈。  

<a id="3.网络结构"></a>
## 3.网络结构
我们提出的物体检测方法被称为定向R-CNN，它由一个定向RPN和一个定向RCNN头部组成（见图2）。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/f688eeac-a296-44c9-ac83-06e717403c7f)  
(图2：有向R-CNN的总体框架，这是一个建立在FPN上的两阶段检测器。第一阶段由有向RPN生成有向proposal，第二阶段是有向R-CNN头部用于分类proposal并细化它们的空间位置。为了清晰起见，我们没有展示有向RPN中的FPN以及分类分支。)

它是一个两阶段检测器，第一阶段以几乎零成本的方式生成高质量的定向proposal，第二阶段是定向RCNN头部用于proposal分类和回归。我们的FPN主干遵循[21]，产生五个级别的特征{P2，P3，P4，P5，P6}。为简单起见，我们没有显示定向RPN中的FPN架构以及分类分支。接下来，我们详细描述定向RPN和定向R-CNN头部。 

<a id="3.1OrientedRPN"></a> 
### 3.1 Oriented RPN
对于任何尺寸的输入图像，定向RPN输出一组稀疏的定向proposal。整个过程可以通过轻量级全卷积网络来建模。具体来说，它将FPN的五个特征级别{P2，P3，P4，P5，P6}作为输入，并为每个特征级别附加相同设计的头部（一个3×3卷积层和两个同级1×1卷积层）。我们在所有特征级别的每个空间位置上分配三个水平anchor，其中包括三个长宽比{1:2，1:1，2:1}的anchor。anchor在{P2，P3，P4，P5，P6}上具有像素面积为{$` {32^{2},64^{2},128^{2},256^{2},512^{2}} `$}。每个anchor用一个4维向量$`a=(a_{x},a_{y},a_{w},a_{h})`$表示，其中$`(a_{x},a_{y})`$是anchor的中心坐标，$`a_{w}`$和$`a_{h}`$表示anchor的宽度和高度。两个同级1×1卷积层中的一个是回归分支：输出相对于anchor的proposal偏移$`{δ=(δ_{x}，δ_{y}，δ_{w}，δ_{h}，δ_{α}，δ_{β})}`$。在特征图的每个位置，我们生成$`A`$个proposal（A是每个位置的anchor数量，并且在本文中等于3），因此回归分支具有$`6A`$个输出。通过解码回归输出，我们可以获得定向proposal。解码过程如下所述（公式1）：

```math
\left\{\begin{matrix}
  &\bigtriangleup\alpha = \delta_{\alpha }\cdot w,\bigtriangleup\beta = \delta_{\beta}\cdot h \\
  &w = a_{w}\cdot e^{\delta_{w}},h = a_{h}\cdot e^{\delta_{h}}&\\
  &x = \delta_{x}\cdot a_{w} + a_{x},y = \delta_{y}\cdot a_{h} + a_{y} &
\end{matrix}\right.
```

其中，$`(x，y)`$是预测proposal的中心坐标，$`w`$和$`h`$是预测定向proposal外部矩形框的宽度和高度。$`\delta_{\alpha }`$和$`\delta_{\beta}`$是相对于外部矩形框顶部和右侧中点的偏移量。最后，我们根据$`(x，y，w，h，\delta_{\alpha }，\delta_{\beta})`$产生定向proposal。

另一个同级卷积层估计每个定向proposal的物体得分。为了清晰地说明，我们在图2中省略了得分分支。定向RPN实际上是一种自然而直观的想法，但其关键在于定向物体的表示方式。在这种情况下，我们设计了一种新的简单的定向物体表示方案，称为中点偏移表示法。

<a id="3.1.1中点偏移表示法MidpointOffsetRepresentation"></a>
#### 3.1.1 中点偏移表示法 Midpoint Offset Representation
我们提出了一种新的定向物体表示方案，称为中点偏移表示法，如图3所示。黑点表示水平框每条边的中点，这是定向边界框O的外接矩形。橙色点表示定向边界框O的顶点。  
![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/ee7d7d0c-5096-4091-91bc-7a4468eed733)    
图3：中点偏移表示法的示意图。 (a) 中点偏移表示法的示意图。 (b) 中点偏移表示法的一个示例。

具体而言，我们使用具有六个参数$`O = (x，y，w，h，\delta_{\alpha }，\delta_{\beta})`$的定向边界框O来表示通过公式（1）计算得到的物体。通过这六个参数，我们可以对于每个proposal获得四个顶点的坐标集合$`v = (v1，v2，v3，v4)`$。这里，$`\delta_{\alpha}`$是$`v1`$相对于水平框顶部的中点$`(x，y - h/2)`$的偏移量。根据对称性，$`-\delta_{\alpha}`$表示$`v3`$相对于底部中点 $`(x，y + h/2)`$的偏移量。$`\delta_{\beta}`$表示$`v2`$相对于右侧中点$`(x + w/2，y)`$的偏移量，$`-\delta_{\beta}`$表示$`v4`$相对于左侧中点$`(x - w/2，y)`$的偏移量。因此，四个顶点的坐标可以表示如下：  
```math
 \left\{\begin{matrix}
 & v1 = (x,y-h/2) + (\bigtriangleup\alpha ,0 ) \\
 & v2 = (x+w/2,y) + (0,\bigtriangleup\beta )& \\
 & v3 = (x,y+h/2) + (-\bigtriangleup\alpha ,0)& \\
 & v4 = (x-w/2,y) + (0,-\bigtriangleup\beta)& \\
\end{matrix}\right.
```

通过这种表示方式，我们通过预测外部矩形的参数$`（x，y，w，h）`$并推断中点偏移的参数$`\delta_{\alpha},\delta_{\beta}`$，对每个定向proposal进行回归。

<a id="3.1.2损失函数LossFunction"></a>
#### 3.1.2 损失函数 Loss Function
为了训练定向RPN，我们定义正样本和负样本如下。首先，给每个anchor分配一个二元标签$`p^{∗} ∈ {0, 1}`$。其中，0和1表示该anchor属于负样本或正样本。具体而言，我们将满足以下条件之一的anchor视为正样本：（i）与任何真实边界框的IoU重叠大于0.7；（ii）与真实边界框的IoU重叠最高且大于0.3。当anchor与真实边界框的IoU小于0.3时，将其标记为负样本。那些既不是正样本也不是负样本的anchor被视为无效样本，在训练过程中被忽略。值得注意的是，上述的真实边界框指的是定向边界框的外接矩形。

接下来，我们定义损失函数L1如下：  
```math
L_{1} = \frac{1}{N}\sum_{i=1}^n F_{cls}(p_{i},{p_{i}^{*}}) + \frac{1}{N}{p_{i}^{*}}\sum_{i=1}^NF_{reg}(\delta_{i},{t_{i}^{*}})
```

这里，$`i`$是anchor的索引，$`N`$（默认为N=256）是一个小批量样本中的总样本数。$`{p_{i}^{*}}`$是第i个anchor的实际标签。$`pi`$是定向RPN分类分支的输出，表示proposal属于前景的概率。$`{t_{i}^{*}}`$是相对于第i个anchor的真实边界框的监督偏移量，是一个参数化的6维向量$`{t_{i}^{*}} = ({t_{x}^{*}},{t_{y}^{*}},{t_{w}^{*}},{t_{h}^{*}},{t_{\alpha}^{*}},{t_{\beta}^{*}}`$，来自于定向RPN回归分支的输出，表示相对于第i个anchor的预测proposal的偏移量。Fcls是交叉熵损失函数。Freg是平滑L1损失函数。对于框回归（参见图4），我们采用仿射变换，其公式如下：  
```math
\left\{\begin{matrix}
  & \delta_\alpha  = \bigtriangleup\alpha /w, \delta_\beta  = \bigtriangleup\beta /h\\
  & \delta_w = log(w/w_a ),\delta _h = log(h/h_a )\\
  & \delta_x = (x-x_a),\delta _y = log(h/h_a )\\
  & t_{\alpha }^{*} = \bigtriangleup\alpha/w_g,t_{\beta }^{*} = \bigtriangleup\beta/h_g\\
  & t_{w }^{*} = log(w_g/w_a),t_{h }^{*} = log(h_g/h_a)\\
  & t_{x}^{*} = (x_g-x_a)/w_a,t_{y}^{*} = (x_g-x_a)/h_a\\
\end{matrix}\right.
```

其中，$`(x_g, y_g)`$、$`wg`$和$`hg`$分别是外接矩形的中心坐标、宽度和高度。$`\bigtriangleup\alpha_g`$和$`\bigtriangleup\beta_g`$是相对于上边和左边中点的偏移量，表示顶部和右侧顶点的位置偏移。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/9d9cd0af-9fd4-4557-86b7-1b10b91b8b0e)  
(图4：框回归参数化的示意图。黑色点是顶边和右边的中点，橙色点是有向边界框的顶点。(a) 锚点。(b) 实际框。(c) 预测框。)

<a id="3.2OrientedR-CNNHead"></a>
### 3.2 Oriented R-CNN Head 
定向R-CNN头部接受特征图{P2，P3，P4，P5}和一组定向proposal作为输入。对于每个定向proposal，我们使用旋转的RoI对齐（简称为旋转RoIAlign）从其对应的特征图中提取一个固定大小的特征向量。每个特征向量经过两个全连接层（FC1和FC2，参见图2），然后是两个并行的全连接层：一个输出proposal属于$`K+1`$类（K个目标类别加上1个背景类）的概率，另一个产生每个$`K`$个目标类别的proposal偏移量。

<a id="3.2.1RotatedRoIAlign"></a>
#### 3.2.1 Rotated RoIAlign 
旋转的RoIAlign是一种从每个定向proposal中提取旋转不变特征的操作。现在，我们根据图5来描述旋转的RoIAlign的过程。由定向RPN生成的定向proposal通常是一个平行四边形（图5中的蓝色框），用参数$`v = (v1，v2，v3，v4)`$表示，其中$`v1，v2，v3`$和$`v4`$是其顶点坐标。为了方便计算，我们需要将每个平行四边形调整为具有方向的矩形。具体来说，我们通过将平行四边形的较短对角线（图5中从v2到v4的线段）延长至与较长对角线具有相同的长度来实现这一点。经过这个简单的操作，我们从平行四边形中得到了定向矩形$`（x，y，w，h，θ）`$（图5中的红色框），其中θ∈[−π/2，π/2]由水平轴和矩形的较长边之间的交角定义。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/e8600762-a3be-409d-b055-0b31bc4ea4be)
(图5：旋转RoIAlign过程的示意图。蓝色框是由有向RPN生成的平行四边形proposal，最左边的红色框是其对应的用于投影和旋转RoIAlign的矩形proposal。)

接下来，我们将定向矩形$`（x，y，w，h，θ）`$投影到步长为$`s`$的特征图$`F`$上，以通过以下操作得到一个旋转的RoI，该旋转的RoI由$`(x_r，y_r，w_r，h_r，θ)`$定义。
```math
\left\{\begin{matrix}
  & w_r = w/s,h_r=h/s\\
  & x_r = \left \lfloor x/s \right \rfloor ,  y_r = \left \lfloor y/s \right \rfloor
\end{matrix}\right.
```

然后，每个旋转的RoI被分成$`m×m`$个网格（m默认为7），以获得尺寸固定的特征图$`F'`$，其维度为m×m×C。对于第c个通道$`（1 ≤ c < C）`$中的索引为$`（i，j）`$ $`（0 ≤ i，j ≤ m-1）`$的每个网格，其值计算如下：
```math
F_{c}^{'}(i,j) = \sum_{(x,y)\in area(i,j)}F_c(R(x,y,\theta ))/n
```

其中，$`F_c`$是第c个通道的特征，$`n`$是每个网格内定位的样本数，而$`area(i, j)`$是包含索引为$`（i，j）`$的网格中的坐标集。$`R（·）`$ 是与[7]相同的旋转变换。

<a id="3.3实现细节ImplementationDetails"></a>
### 3.3 实现细节 Implementation Details
Oriented R-CNN以端到端的方式进行训练，通过同时优化定向RPN和定向R-CNN头部。在推理过程中，定向RPN生成的定向proposal通常具有很高的重叠区域。为了减少冗余，我们在第一阶段保留每个FPN级别的2000个proposal，然后进行非最大值抑制（NMS）处理。考虑到推理速度，采用IoU阈值为0.8的水平NMS。我们将所有级别中剩余的proposal合并，并根据它们的分类分数选择前1000个作为第二阶段的输入。在第二阶段，对那些类别概率大于0.05的预测定向边界框执行多边形NMS。多边形NMS的IoU阈值为0.1。


<a id="4.实验Experiments"></a>
## 4.实验 Experiments
为了评估我们提出的方法，我们在两个最广泛使用的定向目标检测数据集上进行了大量实验，分别是DOTA [36]和HRSC2016 [25]。

<a id="4.1数据集Datasets"></a>
### 4.1 数据集 Datasets
DOTA是一个用于定向目标检测的大规模数据集。它包含2806张图像和188282个具有定向边界框注释的实例，涵盖以下15个目标类别：桥梁（BR）、港口（HA）、船只（SH）、飞机（PL）、直升机（HC）、小型车辆（SV）、大型车辆（LV）、棒球场（BD）、田径场（GTF）、网球场（TC）、篮球场（BC）、足球场（SBF）、环形交叉路口（RA）、游泳池（SP）和储罐（ST）。DOTA数据集的图像尺寸较大，从800×800到4000×4000像素不等。我们使用训练集和验证集进行训练，剩余的用于测试。通过将测试结果提交到DOTA的评估服务器，可以获得检测准确度。

HRSC2016是另一个广泛使用的任意定向船只检测数据集。它包含1061张图像，尺寸从300×300到1500×900不等。训练集（436张图像）和验证集（181张图像）都用于训练，剩余的用于测试。对于HRSC2016的检测准确度，我们采用平均精度均值（mAP）作为评估指标，这与PASCAL VOC 2007 [8]和VOC 2012一致。

<a id="4.2参数设置Parametersettings"></a>
### 4.2 参数设置 Parameter settings
我们在训练过程中使用了一块单独的RTX 2080Ti显卡，批大小为2。推理时间也是在一块单独的RTX 2080Ti上进行测试的。实验结果是在mmdetection平台[3]上产生的。我们使用ResNet50 [14]和ResNet101 [14]作为主干网络。它们在ImageNet [6]上进行了预训练。在训练过程中，采用水平和垂直翻转作为数据增强手段。我们使用带有动量0.9和权重衰减0.0001的SGD算法来优化整个网络。

对于DOTA数据集，我们将原始图像裁剪成1024×1024的小块。裁剪的步长设置为824，即两个相邻小块之间的像素重叠为200。关于多尺度训练和测试，我们首先将原始图像按照三个尺度（0.5、1.0和1.5）进行调整，并将它们裁剪成1024×1024的小块，步长为524。我们使用12个epoch来训练定向R-CNN。初始学习率设置为0.005，在第8和第11个epoch时除以10。当合并图像小块时，Ploy NMS阈值设置为0.1。

对于HRSC2016数据集，我们不改变图像的宽高比。图像的短边被调整为800，而长边小于或等于1333。在训练过程中，采用36个epoch。初始学习率设置为0.005，在第24和第33个epoch时除以10。

<a id="4.3有向RPN的评估EvaluationofOrientedRPN"></a>
### 4.3  有向RPN的评估 Evaluation of Oriented RPN
我们根据召回率评估了有向RPN的性能。有向RPN的结果是在DOTA验证集上报告的，使用ResNet-50-FPN作为主干网络。为了简化过程，我们仅基于从原始图像裁剪的小块计算召回率，而不进行合并。与真实边界框之间的IoU阈值设置为0.5。我们分别从每个图像小块中选择前300、前1000和前2000个候选框来报告它们的召回率，记为R300、R1000和R2000。结果如表1所示。可以看出，当使用2000个候选框时，我们的有向RPN可以达到92.80%的召回率。当候选框的数量从2000个减少到1000个时，召回率仅略微下降（0.6%），但当使用300个候选框时，召回率急剧下降。因此，为了在推理速度和检测准确性之间取得平衡，我们选择1000个候选框作为有向R-CNN头部在测试时的输入，适用于两个数据集。在图6中，我们展示了有向RPN在DOTA数据集上生成的一些候选框示例。每个图像显示了前200个候选框。正如所示，我们提出的有向RPN可以很好地定位对象，无论它们的大小、宽高比、方向和密度如何。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/e69950cc-d2d0-481b-890a-f8a608b3756e)  
(图6：有向RPN在DOTA数据集上生成的proposal。每个图像显示前200个proposal。)

<a id="4.4和SOTA方法相比ComparisonwithState-of-the-Arts"></a>
### 4.4  和SOTA方法相比 Comparison with State-of-the-Arts
我们将我们的有向R-CNN方法与19种有向物体检测方法在DOTA数据集上进行比较，以及在HRSC2016数据集上与10种方法进行比较。表2和表3分别报告了DOTA和HRSC2016数据集上的详细比较结果。主干网如下：R-50代表ResNet-50，R-101表示ResNet-101，H-104是104层的hourglass网络[38]，而DLA-34则表示34层的深度层聚合网络[46]。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/9b161cd8-411b-4d02-8c33-8c24523c874f)  
(表2：在DOTA数据集上与最先进方法的比较。†表示来自AerialDetection的结果（以下相同）。‡表示多尺度训练和测试。)

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/637cb194-88f1-4bdd-bf17-74434ae7e5ff)  
(表3：在HRSC2016数据集上的比较结果。)

在DOTA数据集上，我们的方法超过了所有比较方法。使用R-50-FPN和R-101-FPN作为主干网，我们的方法分别获得了75.87%和76.28%的mAP。令人惊讶的是，即使使用R-50-FPN主干网，我们的方法也胜过所有使用R-101-FPN主干网的比较方法。此外，通过多尺度训练和测试策略，我们的方法使用R-50-FPN主干网达到了80.87%的mAP，与目前最先进的方法相比非常具有竞争力。图7展示了DOTA数据集上的一些结果。

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/b1932690-b7e0-4aa3-a064-526e651d347e)  
(图7：使用带有R-50-FPN主干的有向R-CNN在DOTA数据集上的检测结果示例。在可视化这些结果时，置信度阈值设置为0.3。一种颜色代表一种物体类别。)

![image](https://github.com/Cloud-Jowen/CVPaper_Note/assets/56760687/3fa9031e-3676-4ce3-81ff-8a881ce94d6a)  
(图8：使用带有R-50-FPN主干的有向R-CNN在HRSC2016数据集上的检测结果示例。显示得分高于0.3的有向边界框。 )

对于HRSC2016数据集，我们列出了不同方法在PASCAL VOC 2007和VOC 2012指标下的mAP值。使用R-50-FPN和R-101-FPN，我们的有向R-CNN都获得了最佳精度。一些可视化结果展示在图8中。

<a id="4.5速度与准确性SpeedversusAccuracy"></a>
### 4.5  速度与准确性 Speed versus Accuracy
在相同的设置下，我们比较了不同方法的速度和准确性。比较结果如表4所示。所有方法都采用R-50-FPN作为主干网。测试的硬件平台是单个RTX 2080Ti，批处理大小为1。在测试过程中，输入图像的大小为1024×1024。如表4所示，我们的方法具有更高的检测精度（75.87% mAP），但运行速度相当（15.1 FPS）。有向R-CNN的速度几乎接近一阶段检测器，但准确度远高于一阶段检测器（请参见表4和图9）。

<a id="5.结论Conclusion"></a>
## 5.结论 Conclusion
本文提出了一种实用的两阶段检测器，名为有向R-CNN，用于图像中的任意方向物体检测。我们在两个具有挑战性的有向物体检测基准上进行了大量实验。实验结果表明，与当前先进的两阶段检测器相比，我们的方法具有竞争力的准确性，同时与一阶段有向检测器相比保持了可比较的效率。











