<h1 align="center">mygoFlaskProject</h1>

《mygo》在b站的期间限定公开在10月1日23：03结束了，与此一同消失的还有其中的评论和弹幕:sob:。为了保留两个多月来大家美好的回忆，我在10月1日下午写了个爬虫爬取了评论和弹幕:sunglasses:。本人非前端或后端程序员所以实现的比较简陋（只试了1080和2k的屏幕，并且操作系统的缩放要为100%），之后有时间再重构吧:clipboard:

B站视频地址：https://www.bilibili.com/video/BV1Ww411C73f

## 技术框架

python+flask+dplayer

## mygo,启动!!!!!

首先你得有个python吧，没有就装一个吧，我的python版本是 3.10.11

之后安装requirements.txt里的包

```shell
pip3 install -r requirements.txt
```

由于视频和图片占用的空间较大，这部分我放在网盘

另外评论数据内容很多，为了防止大语言模型的隐私泄露问题，原始评论数据我也放网盘了

代码+资源文件百度链接：链接：https://pan.baidu.com/s/12-9FFjBTDpEviTlfYkx_vg 提取码：m588

竟然还有很多非技术的粉丝关注这个项目，那我再放一下python运行环境的网盘：https://pan.baidu.com/s/1uuHwohQThnb0JkYmBP7wFA  提取码：2yg4

（本来以为没人用谷歌云盘，没想到这么多，二合一谷歌云盘链接https://drive.google.com/file/d/1cWe6gwOBdhbCWBCgPUWD8V5ZkFxYM1yu/view?usp=sharing  ,解压后直接双击运行里面的run.bat即可）

主要缺少以下文件的内容

- mygoFlaskProject/video/
- mygoFlaskProject/static/pic/
- mygoFlaskProject/get_data/comment_json/

如果你有更高清的视频资源和更全的弹幕资源也可以用你自己的，补全文件后就可以愉快的启动了

```shell
python app.py
```
首页效果
![播放器效果](https://github.com/wangwc18/mygoFlaskProject/blob/master/show-player.png)
评论区效果
![评论区效果](https://github.com/wangwc18/mygoFlaskProject/blob/master/show-comment.png)

评论区上的图片（跳转主题页）和视频播放器右侧的图片（跳转b站会员购）都是可以点击跳转到对应的页面

## 项目结构

**数据获取**

1. 弹幕使用“唧唧Down”获取xml和ass文件，只用xml文件，这些文件在mygoFlaskProject/danmaku/（做了重命名）
2. 同时下载了视频文件在mygoFlaskProject/video/（做了重命名）
3. 剩余的数据为程序抓取，在mygoFlaskProject/get_data/目录下
   - get_comment.py获取评论信息，保存在comment_json文件夹下（已经修改为抓最新评论，抓最热评论同理可得）
   - get_pic.py根据comment_json中所有json信息下载需要的图片
   - 原始json信息太多，使用orginal_json_to_type.py把comment_json中的json转换为mygoFlaskProject/comment_hot_json/和mygoFlaskProject/comment_new_json/,对应最热和最新评论

**视频组件**

经过b站月落云尘大佬指路，本分支视频组件替换为使用nplayer( https://github.com/oyuyue/nplayer )，
原本的项目是使用dplayer( https://github.com/DIYgod/DPlayer )，但是有bug迟迟不能修复。后续再研究一下添加新的功能



剩下的写的都比较简陋(~~实在太懒~~)了:grin:，有机会用Vue重构一下前端吧(大概要等到Mujicac出了吧，欸嘿:star:)
