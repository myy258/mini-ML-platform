# Mini ML Platform
## 迷你机器学习平台
本平台旨在可以快速查看数据分布和进行机器学习任务。内置少量机器学习模型，统计分析方法和数据可视化。引入大模型解读数据并提出建议。

## 使用环境

- **Python版本**: 3.10.19
- **Conda**: Miniforge

## 主要模块版本

- **pandas**: 2.3.3
- **numpy**: 2.2.6
- **matplotlib**: 3.10.9
- **openpyxl**: 3.1.5
- **PyQt5**: 5.15.11
- **scikit-learn**: 1.7.2
- **transformers**: 5.3.0
- **torch**: 2.7.1+cu118

## 界面示例

![image](https://github.com/myy258/MINI-DATA-ANALYSIS-PLATFORM/blob/master/img/Screenshot%202026-04-27%20154809.png)
![image](https://github.com/myy258/MINI-DATA-ANALYSIS-PLATFORM/blob/master/img/Screenshot%202026-04-27%20155150.png)
![image](https://github.com/myy258/mini-ML-platform/blob/master/img/Screenshot%202026-05-21%20090129.png)


## 功能介绍
- **可导入excel文件。无法在本平台处理数据。只可对字段进行排序**
- **可进行机器学习分类和回归任务，可导出导入模型。模型可以调参，但可用参数有限**
- **可生成一组或多组图标，可视化模块的XY轴可多选**
- **可本地部署大模型，根据电脑配置部署不同规模的大模型，本用例使用的是Qwen3-0.6B。大模型可解读分析结果**

## 相关更新
- 5.21 - 新增ensemble model模块和LLM模块

## 备注

目前DEMO可用，后续有空再更新。计划加入更多机器学习模型和一些数据清洗功能，考虑开发可调用本地LLM和线上LLM的模块。

