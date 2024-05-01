<h1 align="center">mygoFlaskProject</h1>

自上次2023.10.01《mygo》在B站下架后，为了保留大家在B站观看mygo的美好回忆，我爬取了评论和弹幕制作了这个可以本地启动的网页项目。2024.04.08-2024.04.17为了庆祝活动mygo又再次短暂上架，我对数据进行了更新，页面做了重构。

B站视频地址：https://www.bilibili.com/video/

往期回顾：https://www.bilibili.com/video/BV1Ww411C73f

## 技术框架

python+flask+bootstrap+nplayer

## mygo，启动!!!!! （按照以下四种情况下载对应的资源进行操作即可）
百度云盘：链接：https://pan.baidu.com/s/1rlRCLZ8B32ozVbnlrGeggg?pwd=eyrw 提取码：eyrw

谷歌云盘：https://drive.google.com/drive/folders/1hOLUy8toxSi63UbNCoDNCAE9dRwuDbia?usp=sharing

### 不包含本地视频资源与本地图片资源(下载体积最小)：
你有mygo的视频资源，不想下载评论区图片，则程序评论区图片使用b站的图片地址，所以启动程序时电脑需要联网，否则图片都会加载失败。一些图片可能失效或被更改
  1. 下载对应文件夹里的压缩包
  2. 解压到任意位置
  3. 打开解压后的mygoFlaskProject文件夹，找到mygoFlaskProject/video文件夹，把视频资源放入其中(支持MP4/WebM/Ogg/FLV/AVI/MKV/MOV/...等类型的文件，具体可能还要看一下视频编码格式)，注意在windows默认排序下需要满足“1-12集、总集篇、13集、特别节目1-2”这个顺序，否则会导致集数错乱，如果错乱的话可以按1-16重命名视频文件，缺少的资源可以在网盘“视频资源”里下载
  4. 双击"windows一键启动.bat"打开命令行，打开浏览器(最好是谷歌)输入`127.0.0.1:5000`访问
### 不包本地含视频资源包含本地图片资源：
你有mygo的视频资源，希望下载评论区图片
  1. 下载对应文件夹里的压缩包
  2. 解压到任意位置
  3. 打开解压后的mygoFlaskProject文件夹，找到mygoFlaskProject/video文件夹，把视频资源放入其中(支持MP4/WebM/Ogg/FLV/AVI/MKV/MOV/...等类型的文件，具体可能还要看一下视频编码格式)，注意在windows默认排序下需要满足”1-12集、总集篇、13集、特别节目1-2“这个顺序，否则会导致集数错乱，如果错乱的话可以按1-16重命名视频文件，缺少的资源可以在网盘“视频资源”里下载
  4. 双击"windows一键启动.bat"打开命令行，打开浏览器(最好是谷歌)输入`127.0.0.1:5000`访问
### 包含本地视频资源不包含本地图片资源：
你没有mygo的视频资源，不想下载评论区图片。则程序的评论区图片使用b站的图片地址，所以启动程序时电脑需要联网，否则图片都会加载失败。一些图片可能失效或被更改
  1. 下载对应文件夹里的压缩包
  2. 解压到任意位置
  3. 双击"windows一键启动.bat"打开命令行，打开浏览器(最好是谷歌)输入`127.0.0.1:5000`访问
### 包含本地视频资源与本地图片资源(下载体积最大)：
你没有mygo的视频资源，希望下载”视频资源“和”评论区图片“
  1. 下载对应文件夹里的压缩包
  2. 解压到任意位置
  3. 双击"windows一键启动.bat"打开命令行，打开浏览器(最好是谷歌)输入`127.0.0.1:5000`访问




**常见问题：**
   - 缺少视频资源，在云盘中找到"视频资源"文件夹下载后放在mygoFlaskProject/video文件夹下
   - 视频有声音黑屏：说明自己准备的视频是v265格式，这个目前只有新的浏览器支持，下载安装谷歌浏览器解决，谷歌官网是 https://www.google.cn/chrome/index.html ，不要进到钓鱼网站了
   - 视频不加载+评论区不加载：原因是火绒的拦截策略，临时关掉火绒或者b站私聊，改一下代码即可
   - 页面布局错乱：浏览器最大化后调整网页缩放即可
   - 感觉视频不够清楚：mygoFlaskProject/video/文件夹下放的是所有视频，替换为你的高清资源即可（这里推荐一个阿里云盘资源: https://www.aliyundrive.com/s/4vHPUhfMMEK 提取码: ja76 ）
   - 运行后图片和视频加载慢：不要把文件夹放在U盘或其他移动存储设备中直接运行，会导致数据传输受制于接口速度，如果还是卡那可能你需要换个新电脑啦:grin:
   - 想在手机或pad上运行：没问题，但是移动端的页面没有适配，操作方法是手机和电脑连接同一wifi(在同一个局域网内)，电脑打开程序后，手机浏览器（最好也是谷歌）访问命令行中的第二个地址，注意在播放视频时最好使用横屏模式。

## 开发环境启动
1. 下载文件
   * 你可以直接从上面的两个网盘下载本仓库的完整版本。
   * 你也可以通过 `git clone git@github.com:wangwc18/mygoFlaskProject.git` 命令克隆本仓库。但是你还是需要从网盘下载完整版压缩包，解压后将文件夹拷贝覆盖到本仓库下（缺少视频资源与图片资源）。
2. python环境启动
   * Step 1: 首先你得有个python吧，没有就装一个吧，我的python版本是 3.10.11
   * Step 2: 之后安装requirements.txt里的包，在文件夹下打开命令行，输入
     ```shell
     pip3 install -r requirements.txt
     ```
   * Step 3: 命令行启动程序
     ```shell
     python app.py
     ```
3. conda环境启动
   * Step 1: 新建 conda 环境，使用如下命令：
     * `conda create -n mygo python=3.10`
     * `conda activate mygo`
     * `pip install -r requirements.txt`
   * Step 2: 启动 app.py
       * `python app.py`
       * 此时如果遭遇端口号被占用的问题，请编辑 `run_mode.json`，将最后一行的 `"port":` 改为一个你喜欢的四位数。
       * 使用 Chrome 访问 `127.0.0.1:上面设置的端口号`，就可以看 mygo 了。
   
4. 效果：
   * 首页效果
      ![alt text](show-player.png)
   * 评论区效果
      ![alt text](show-comment.png)
   * 活动页效果（视频播放器右侧广告区域点击跳转到这个页面）
      ![alt text](show-mygo.png)

## 项目结构

### 数据获取

1. 弹幕有三种来源，这些文件在mygoFlaskProject/danmaku/ 下（做了重命名）
   - 标准弹幕(1文件夹)，使用“唧唧Down”获取xml和ass文件，只用xml文件
   - 最多弹幕(2文件夹)，使用b站的这篇专栏 https://www.bilibili.com/read/cv26903973/ ，作者做了最大合并，里头还有各种其他类型的弹幕
   - 开播弹幕(3文件夹)，后期弹幕和前期弹幕的观感不同（比如前期弹幕剧透更少），所以取了前3000条，这部分由Gray Zhang提供
2. 同时下载了视频文件在mygoFlaskProject/video/下
3. 剩余的数据为程序抓取，保存在mygoFlaskProject/get_data/目录下
   - get_basic_mess.py 获取视频的基础信息（类似标题、播放数量、弹幕数量等）生成mygoFlaskProject/basic.json
   - get_comment.py 获取所有评论以及回复，生成三个文件夹comment_json_hot、comment_json_new、comment_json_more，分别对应最热评论、最新评论、更多评论的原始json。为了防止大语言模型的隐私泄露问题，原始评论数据我放网盘了。（PS:由于04.17晚上cookie过期导致爬取失败，现在的数据是04.17下午2点爬的，红豆泥斯米马赛。。。。。）
   - get_pic.py 爬取评论区图片
   - orginal_json_to_type.py 原始json信息太多，把信息精简后放在mygoFlaskProject/下
     - comment_hot_json 最热评论(json中的图片链接为本地图片链接)
     - comment_new_json 最新评论(json中的图片链接为本地图片链接)
     - comment_more_json 更多评论，评论回复中的“点击查看”加载出的评论(json中的图片链接为本地图片链接)
     - comment_hot_json_online 最热评论(json中的图片链接为B站链接)
     - comment_new_json_online 最新评论(json中的图片链接为B站链接)
     - comment_more_json_online 更多评论，评论回复中的“点击查看”加载出的评论(json中的图片链接为B站链接)

### 视频组件
1. 本分支视频组件替换为使用nplayer( https://github.com/oyuyue/nplayer )，
原本的项目是使用dplayer( https://github.com/DIYgod/DPlayer )，但是有bug迟迟不能修复。后续再研究一下添加新的功能
2. 弹幕的用户播放配置写入cookie，但是由于bug弹幕的透明度无法保存

## 最后
- 超级感谢b站月落云尘大佬对nplayer视频组件的指路以及代码示范
- 感谢b站Darklyyy对页面部分细节的优化，之前一个2k屏幕适配的分支：https://github.com/wangwc18/mygoFlaskProject/tree/better2k
- 感谢github的Gray Zhang大佬( https://github.com/otakustay )提供的新弹幕文件和建议

剩下的写的都比较简陋(~~实在太懒~~) ，有机会用Vue重构一下前端吧(大概要等到Mujicac出了吧，欸嘿)

母鸡卡要25年1月啦？？？？？！！！！！
