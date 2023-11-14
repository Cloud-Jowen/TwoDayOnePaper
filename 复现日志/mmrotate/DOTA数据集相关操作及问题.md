# 操作
## 操作1 切分 DOTA 数据集

# 问题
### 问题1 对 DOTA 测试集进行测试时，计算 mAP 出现问题

训练命令：此处 {} 表示未填写的实际路径
```
python .tools/test.py  \
  {config.py} \
  {checkpoint.pt} \
  --work-dir {output_file} \
  --eval mAP 
```
报错提示：
```
  File "/mnt/sdb1/jsy/yjw/Jowen/mmrotate/tools/test.py", line 271, in <module>
    main()
  File "/mnt/sdb1/jsy/yjw/Jowen/mmrotate/tools/test.py", line 263, in main
    metric = dataset.evaluate(outputs, **eval_kwargs)
  File "/mnt/sdb1/jsy/yjw/Jowen/mmrotate/mmrotate/datasets/dota.py", line 202, in evaluate
    mean_ap, _ = eval_rbbox_map(
  File "/mnt/sdb1/jsy/yjw/Jowen/mmrotate/mmrotate/core/evaluation/eval_map.py", line 177, in eval_rbbox_map
    cls_dets, cls_gts, cls_gts_ignore = get_cls_results(
  File "/mnt/sdb1/jsy/yjw/Jowen/mmrotate/mmrotate/core/evaluation/eval_map.py", line 114, in get_cls_results
    cls_gts.append(ann['bboxes'][gt_inds, :])
TypeError: list indices must be integers or slices, not tuple
```
报错原因：  
定位到目标函数
```python
def get_cls_results(det_results, annotations, class_id):
    """Get det results and gt information of a certain class.

    Args:
        det_results (list[list]): Same as `eval_map()`.
        annotations (list[dict]): Same as `eval_map()`.
        class_id (int): ID of a specific class.

    Returns:
        tuple[list[np.ndarray]]: detected bboxes, gt bboxes, ignored gt bboxes
    """
    cls_dets = [img_res[class_id] for img_res in det_results]

    cls_gts = []
    cls_gts_ignore = []
    for ann in annotations:
        gt_inds = ann['labels'] == class_id
        cls_gts.append(ann['bboxes'][gt_inds, :])

        if ann.get('labels_ignore', None) is not None:
            ignore_inds = ann['labels_ignore'] == class_id
            cls_gts_ignore.append(ann['bboxes_ignore'][ignore_inds, :])

        else:
            cls_gts_ignore.append(torch.zeros((0, 5), dtype=torch.float64))

    return cls_dets, cls_gts, cls_gts_ignore
```
报错语句为：`cls_gts.append(ann['bboxes'][gt_inds, :])`  
该问题是对 DOTA 测试集进行切分之后，部分图片检测不到目标，导致 gt_inds 为 False，进而导致语句报错  
经输出 `annotations` 和 `class_id` 后可发现
`annotations(部分) = [{'bboxes': [], 'labels': []}, {'bboxes': [], 'labels': []}, {'bboxes': [], 'labels': []}, {'bboxes': [], 'labels': []}]
class_id = 0`


解决办法：
