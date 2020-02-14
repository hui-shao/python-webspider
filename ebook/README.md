# 爬虫-电子课本
用于下载"书链"的电子课本，例如:

> https://mp.codeup.cn/book/shelf.htm?id=2529&mallId=263

### 主要特征

- 支持 自动获取书架上所有书的信息，仅需传入 shelf_id
- 支持 自动建立目录(以书本名为目录名)
- 支持 按照页码顺序，自动重命名图片序列
- 支持 自动保存出错链接 到 每本书的下载目录中的errors.txt
- 兼容 Windows 、Linux

### 使用说明

1. 修改 'main.py' 中的 'shelf_ids = []' ，上述链接中，shelf_id 为 2529
2. 在终端中运行 main.py