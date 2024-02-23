

## 使用说明

### 1、选取区域

1. 打开Open the [Hello World example in Sandcastle](https://sandcastle.cesium.com/)

![image-20230721105355444](https://raw.githubusercontent.com/shiner-chen/imgbed/main/image-20230721105355444.png)

2. copy area_select.js文件内容替换上图中javaScript脚本，点击run

   ![image-20230721105612786](https://raw.githubusercontent.com/shiner-chen/imgbed/main/image-20230721105612786.png)

3. 在画面右上方，点击放大镜，输入目的地名称，例如：台北，然后点击放大镜进行搜索

   ![image-20230721110018508](https://raw.githubusercontent.com/shiner-chen/imgbed/main/image-20230721110018508.png)

4. 按下shift键不放，然后按下鼠标左键，拖动选取要下载的区域，在下方的console页中，最后一行是你选取的区域范围的经纬度范围

   ![image-20230721110234030](https://raw.githubusercontent.com/shiner-chen/imgbed/main/image-20230721110234030.png)

### 2. 运行Downloader.py对选定区域的瓦片数据进行下载

```
$python3 Downloader.py
```

参数
   -s --south  必选，选取区域的下边纬度值

   -n --north 必选，选取区域的上边纬度值

   -w --west 必选，选取区域的左边经度值

   -e  --east 必选，选取区域的右边经度值

   -d --dir  必选，需要保存的目录

   -k --key 必选  google map API key, 如何申请google map API key，请参考[图文详解申请谷歌地图API密钥](http://www.krpano360.com/tuwenxiangjieshenqinggugedituapimiyao/)

示例：

python Downloader.py -s 25.035368204527927 -n 25.037106020904716 -w 121.53962207411472 -e 121.541969503934 -k <your google map api key>  -d D:\3dtiles\download



python GridGenerate.py -s 25.037841127 -n 25.0433358983 -w 121.250609505 -e 121.256104276 -g test.json

python Downloader.py -s 25.037841127 -n 25.0433358983 -w 121.250609505 -e 121.256104276 -k AIzaSyD-sJKuhCVqR6bpkRWBgTyxnszApF9_U-M -d D:\3dtiles\download

### 替换文件中uri路径
```
sed -i "s/\/v1\/3dtiles\/datasets\/CgA\/files\///g" `find -name "*.json"`
```

