# 项目概述

书籍推荐助手

# 主要功能

### 文段来源查找

给定一段文字，查找来源于哪本书。支持图片查找。

### 作者信息查询

给出作者名，搜索作者相关信息。

### 书籍推荐

给出推荐要求，通过多种方法搜索，多维度评分，最后给出最符合要求的书籍。

# 部署指南

### 前置条件

克隆项目`git clone https://github.com/C1942hjx/AI-Basic-Homework.git`。

python 版本 3.10。

需要安装 camel-ai 0.2.38 版本，以及相应的依赖。其余依赖见  requirements.txt。

### 环境配置

在 `main.py` 所在目录中，将 `.env.example` 文件重命名为 `.env` 文件。并按照提示，填入 Deepseek 模型和 Qwen 模型的 API Key 以及 URL。如果希望使用 Google 搜索，则需要填入 Google API Key 以及 URL。

项目需要使用 `intfloat/e5-small-v2` 作为嵌入模型进行向量检索，请前往 [Hugging Face 官网](https://huggingface.co/) 或者 [镜像网站](https://hf-mirror.com/) 进行下载。具体步骤可以参考 [这篇文章](https://zhuanlan.zhihu.com/p/663712983)。将下载好的模型文件夹命名为 `e5-small-v2`，并放在 `main.py` 所在目录中。

upd: 现在仓库中已有 `e5-small-v2` 模型。
