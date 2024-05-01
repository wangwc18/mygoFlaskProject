<h1 align="center">mygoFlaskProject</h1>

《mygo》在b站的期间限定公开在10月1日23：03结束了，与此一同消失的还有其中的评论和弹幕。为了保留两个多月来大家美好的回忆，我在10月1日下午写了个爬虫爬取了评论和弹幕。本人非前端或后端程序员所以实现的比较简陋（我在1080p的屏幕100%系统缩放100%网页缩放下测试的，2k屏可以看一下此项目的better2k分支），之后有时间再重构吧。。。。。。

B站视频地址：https://www.bilibili.com/video/BV1Ww411C73f


## 技术框架

python+flask+nplayer

## mygo,启动!!!!!
1. 下载、解压、直接启动!!!!!
   
   **本来B站视频里介绍的两个下载链接，但是实践后发现还不够简单，现在只需要下载链接中的一个压缩包**，解压之后可以放在任何地方，之后直接双击运行里面的run.bat即可。

   代码+资源文件+运行环境 百度链接： https://pan.baidu.com/s/1wnc1_61e2xlmMXSUNvPFIg  提取码：nsxo

   本来以为国内没人用谷歌云盘，没想到这么多，放一个谷歌云盘链接 https://drive.google.com/drive/folders/1hOLUy8toxSi63UbNCoDNCAE9dRwuDbia?usp=sharing

   常见问题：
   - 视频有声音黑屏：下载或更新至最新的谷歌浏览器即可，压缩包里的视频是v265格式，目前只有新的浏览器支持，谷歌官网是 https://www.google.cn/chrome/index.html ，不要进到钓鱼网站了
   - 如果最新的谷歌浏览器也黑屏，下载这个 https://www.alipan.com/s/w1p8wp5K3kZ
把这个video文件夹下好之后，替换mygoFlaskProject里的video文件夹应该可以了，这个是老视频编码，而且更清晰
   - 视频不加载+评论区不加载：原因是火绒的拦截策略，临时关掉火绒或者b站私聊，改一下代码即可
   - 页面布局错乱：调整网页缩放即可
   - 感觉视频不够清楚：mygoFlaskProject/video/文件夹下放的是所有视频，替换为你的高清mp4资源即可（ https://www.alipan.com/s/w1p8wp5K3kZ ）
   - 运行后图片和视频加载慢：不要把文件夹放在U盘或其他移动存储设备中直接运行，会导致数据传输受制于接口速度，如果还是卡那可能你需要换个新电脑啦:grin:
   - 想在手机或pad上运行：没问题，但是移动端的页面没有适配，操作方法是手机和电脑连接同一wifi(在同一个局域网内)，电脑打开程序后，手机浏览器（最好也是谷歌）访问命令行中的第二个地址，注意在播放视频时最好使用横屏模式。

2. 开发环境启动

   首先你得有个python吧，没有就装一个吧，我的python版本是 3.10.11

   之后安装requirements.txt里的包

   ```shell
   pip3 install -r requirements.txt
   ```
   
   由于视频和图片占用的空间较大，这部分我放在网盘
   
   另外评论数据内容很多，为了防止大语言模型的隐私泄露问题，原始评论数据我也放网盘了
   
   主要缺少以下文件的内容
   
   - mygoFlaskProject/video/
   - mygoFlaskProject/static/pic/
   - mygoFlaskProject/get_data/comment_json/
   
   如果你有更高清的视频资源和更全的弹幕资源也可以用你自己的，补全文件后就可以愉快的启动了
   
   ```shell
   python app.py
   ```
   
3. 效果：

   首页效果
   ![alt text](show-player.png)
   评论区效果
   ![alt text](show-comment.png)
   活动页效果（评论区上的图片点击跳转）
   ![alt text](show-mygo.png)
   视频播放器右侧的图片（跳转b站会员购）都是可以点击跳转到B站对应的页面
   
## Mac + conda 运行本项目

* Step 1: 克隆本项目。
   * 你可以直接从谷歌云盘 [https://drive.google.com/drive/folders/1hOLUy8toxSi63UbNCoDNCAE9dRwuDbia?usp=sharing
   ](https://drive.google.com/drive/folders/1hOLUy8toxSi63UbNCoDNCAE9dRwuDbia?usp=sharing
   ) 下载本仓库的完整版本。
   * 你也可以通过 `git clone git@github.com:wangwc18/mygoFlaskProject.git` 命令克隆本仓库。但是你还是需要从谷歌云盘下载完整版压缩包，解压后将 `video/` `static/pic/` 和 `get_data/comment_json/` 文件夹拷贝到本仓库下。
* Step 2: 新建 conda 环境，使用如下命令：
    * `conda create -n mygo python=3.10`
    * `conda activate mygo`
    * `pip install -r requirements.txt`
* Step 3: 启动 app.py
    * `python app.py`
    * 此时如果遭遇端口号被占用的问题，请编辑 `app.py`，将最后一行的 `port=` 改为一个你喜欢的四位数。
    * 使用 Chrome 访问 `127.0.0.1:上面设置的端口号`，就可以看 mygo 了。

![alt text](show-mac-mygo.png)
    
以上测试使用 mac 环境 Ventura 13.4, MacBook Air M1，Chrome 121.0.6167.160.

## 项目结构

**数据获取**

1. 弹幕有三种来源，这些文件在mygoFlaskProject/danmaku/（做了重命名）下，最近才发现原来历史弹幕还能访问？这几天再试试！！！
   - 标准弹幕，使用“唧唧Down”获取xml和ass文件，只用xml文件
   - 最多弹幕，使用b站的这篇专栏 https://www.bilibili.com/read/cv26903973/ ，作者做了最大合并，里头还有各种其他类型的弹幕
   - 开播弹幕，后期弹幕和前期弹幕的观感不同（比如前期弹幕剧透更少），所以取了前3000条，这部分由Gray Zhang提供
2. 同时下载了视频文件在mygoFlaskProject/video/（做了重命名）
3. 剩余的数据为程序抓取，在mygoFlaskProject/get_data/目录下
   - get_comment.py获取评论信息，保存在comment_json文件夹下（已经修改为抓最新评论，抓最热评论同理可得）
   - get_pic.py根据comment_json中所有json信息下载需要的图片
   - 原始json信息太多，使用orginal_json_to_type.py把comment_json中的json转换为mygoFlaskProject/comment_hot_json/和mygoFlaskProject/comment_new_json/,对应最热和最新评论

**视频组件**
1. 本分支视频组件替换为使用nplayer( https://github.com/oyuyue/nplayer )，
原本的项目是使用dplayer( https://github.com/DIYgod/DPlayer )，但是有bug迟迟不能修复。后续再研究一下添加新的功能
2. 弹幕的用户播放配置写入cookie，但是由于bug弹幕的透明度无法保存

**最后**
- 超级感谢b站月落云尘大佬对nplayer视频组件的指路以及代码示范
- 感谢b站Darklyyy对页面部分细节的优化，2k屏幕更好的适配可以看看这个分支：https://github.com/wangwc18/mygoFlaskProject/tree/better2k
- 感谢github的Gray Zhang大佬( https://github.com/otakustay )提供的新弹幕文件和建议


剩下的写的都比较简陋(~~实在太懒~~) ，有机会用Vue重构一下前端吧(大概要等到Mujicac出了吧，欸嘿)

母鸡卡要25年1月啦？？？？？
