# ISO-DVD-Filler
将小型 ISO 镜像空白填充至标准 DVD5/DVD9 物理容量，含 Python 桌面 GUI 工具，仅填充、不改变原有镜像内容。

- DVD5：4.7GB（单层 DVD）
- DVD9：8.5GB（双层 DVD）

通过 ISO 尾部空白填充，使刻录数据区域接近 DVD 物理容量，从而减少 DVD-R 刻录后的盘面区域差异，同时保持原始 ISO 内容完全不变。

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

## 工作原理

1. 读取输入 ISO 的实际大小（字节）。
2. 根据目标光盘类型计算标准容量
3. 将输入 ISO 完整复制到输出文件，然后追加足够数量的 \x00 字节，使输出文件大小等于目标容量。
4. 不修改原始 ISO 的任何内部结构，仅扩展物理大小。

## 注意事项
1. 请确保目标磁盘空间足够。  
2. 输出 ISO 文件需要额外占用完整 DVD 容量空间。  
3. 不建议覆盖原始 ISO 文件。  
4. 填充后的 ISO 适合刻录到对应容量 DVD 光盘。


## 开源许可与使用限制
ISO-DVD-Filler 仅用于 ISO 容量填充，不包含任何版权内容处理功能。  
用户应确保对所处理的 ISO 镜像拥有合法使用权限。  
未经作者明确书面授权，禁止将本软件用于任何商业活动  
如果您希望将 ISO-DVD-Filler 用于商业用途，请联系作者获取商业授权。  

## ps:
最近沉迷DIY光盘，发现刻录过的区域和没有刻录数据的区域会有很明显的色差，在光盘上会有很明显的颜色区分，对于追求作品质量的作者来说是万万不能接受的，查遍全网也没找到类似的项目（更可能是我没找到），所以只能自己动手了。Audio CD原理和DVD不一样，不能使用类似的方法消除色差。
