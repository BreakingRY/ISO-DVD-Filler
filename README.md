# ISO-DVD-Filler
将小型 ISO 镜像空白填充至标准 DVD5/DVD9 物理容量，含 Python 桌面 GUI 工具，仅填充、不改变原有镜像内容。

- DVD5：4.7GB（单层 DVD）
- DVD9：8.5GB（双层 DVD）

本工具仅进行容量填充，不修改、不压缩、不重建 ISO 内部文件结构，确保原始镜像内容保持完全不变。

适用于需要将 ISO 镜像刻录至实体 DVD 光盘的场景，例如：

- 系统安装光盘制作
- 软件归档光盘制作
- 数据备份光盘制作
- 需要固定 DVD 容量的镜像分发

## 功能特点

- ✅ ISO 镜像无损填充
- ✅ 不修改原始 ISO 文件内容
- ✅ 支持 DVD5 / DVD9 标准容量
- ✅ 支持命令行模式
- ✅ 提供 Windows 桌面 GUI 工具
- ✅ 操作简单，适合普通用户使用
- ✅ 填充数据为空白区域，不影响 ISO 可读性


## 文件说明


ISO-DVD-Filler/  
│ 
├── ISO-DVD-Filler.exe # Windows GUI 程序（由 iso_fill_gui.py 打包）  
├── README.md # 使用说明  
├── iso_fill.py # 命令行版本  
└── iso_fill_gui.py # Python GUI 版本  




## 使用方法

### 方法一：GUI 图形界面

#### 运行：


ISO-DVD-Filler.exe


#### 选择：

1. 选择源ISO文件
2. 设置输出 ISO 文件
3. 选择碟片规格：
   - DVD5
   - DVD9
4. 开始填充
   
程序会自动生成填充后的 ISO 文件。


### 方法二：命令行模式
#### 查看帮助

```bash
python iso_fill.py -h
```
#### 使用示例

1. 填充为单层 DVD5（4.7G 标准）
```bash
python iso_fill.py -i source.iso -o filled_dvd5.iso -d dvd5
```
2. 填充为双层 DVD9（8.5G 标准）
```bash
python iso_fill.py -i source.iso -o filled_dvd9.iso -d dvd9
```
   
