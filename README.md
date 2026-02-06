# Just a bunch of random tools - 只是一堆随意的工具

注意：dev分支非常不稳定，它就是一块试验田。事实上目前为止main分支也不太稳定，毕竟不久前这个项目还是我自己的试验田。  
如题，原本只是个人用的一些小工具，后来想着做都做了，开源也没啥的

| ![png2jpg.png](readme_assets/png2jpg.png)       | ![upscaler.png](readme_assets/upscaler.png) |
|-------------------------------------------------|---------------------------------------------|
| ![similarity.png](readme_assets/similarity.png) | ![flatten.png](readme_assets/flatten.png)   |

## 当前功能

- 展平文件夹
- PNG 转 JPG
- 图像序列转 PDF
- ComfyUI 图像放大
- 截取文本
- 计算相似度
- JSON 排序
- 生成噪声图像
- 导出 Qt 内置图标
- 设置主题

## 部署

推荐使用虚拟环境
1. 克隆这个仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行`app.py`

## 开发计划
- [x] 把所有功能的反馈模式改为消息框
- [ ] 实现并应用统一的 ErrorCode 类 👈 **正在进行**
- [ ] 为 ErrorCode 类增加 lvl 以实现等级区分，分清警告和错误
- [ ] 新增：视频裁剪