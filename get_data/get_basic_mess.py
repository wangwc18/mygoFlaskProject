import json
import requests
from lxml import etree

"""
视频的基础信息（类似标题、播放数量、弹幕数量等）爬取脚本
"""

# 爬取的视频bid列表
bid_list = [
    'BV1Zu4y1B7DU',
    'BV1xV41137an',
    'BV1nV41137kJ',
    'BV14V4y1v7pb',
    'BV1ah4y1k7jm',
    'BV1eh4y1k78d',
    'BV1dj411z7FW',
    'BV1k94y1r7o1',
    'BV1M8411d7Dj',
    'BV1Wm4y1H7Vt',
    'BV11F411C79G',
    'BV1Vm4y1M7mX',
    'BV1Yh4y1K77V',
    'BV1iz4y1j7xY',
    'BV1yk4y1F7fC',
    'BV1KN4y1f7wg'
]
# mygo关注:36.5万 列表:1178.0万播放

# 简介下方tab标签
tab_list = [
    ['动画','综合 MyGO!!!!!','立石凛','青木阳菜','小日向美香','mygo','高尾奏音','BanG Dream!','林鼓子','羊宫妃那'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','灯','爱音','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['碧天伴走','动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','灯','爱音','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['詩超絆','动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','爱音','灯','BanG Dream!'],
    ['动画','综合','MyGO!!!!!','mygo','BanG Dream!'],
    ['动画','综合','乐奈','MyGO!!!!!','mygo','立希','爽世','灯','爱音','BanG Dream!'],
    ['动画','综合','立石凛','青木阳菜','小日向美香','MyGO!!!!!','mygo','Ave Mujica','高尾奏音','BanG Dream!','林鼓子','羊宫妃那'],
    ['动画','综合','立石凛','青木阳菜','小日向美香','MyGO!!!!!','mygo','Ave Mujica','高尾奏音','BanG Dream!','林鼓子','羊宫妃那'],
]
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip,deflate,br,zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
video_dic = {}
rank = 1
for bid in bid_list:
    page_url = "https://www.bilibili.com/video/"+bid
    shuiyun_html = requests.get(page_url, headers=header).content
    # 解析html页面dom树，需要注意只有原本页面里的信息才可以爬，动态加载出来的元素是找不到的
    dom_tree = etree.HTML(shuiyun_html, parser=etree.HTMLParser(encoding='utf-8'))
    # 单个视频的信息字典
    video_dic_item = {'rank': rank,  # 列表中排序
                      'title': dom_tree.xpath('//*[@id="viewbox_report"]/div[1]/div/h1')[0].text,  # 视频标题
                      'play_time': dom_tree.xpath('//*[@id="viewbox_report"]/div[2]/div/div[1]/div')[0].text,  # 播放数量
                      'danmaku_num': dom_tree.xpath('//*[@id="viewbox_report"]/div[2]/div/div[2]/div')[0].text,  # 弹幕数量
                      'upload_time': dom_tree.xpath('//*[@id="viewbox_report"]/div[2]/div/div[3]/div')[0].text,  # 上传时间
                      'des': dom_tree.xpath('//*[@id="v_desc"]/div[1]/span')[0].text,  # 视频简介
                      'like': dom_tree.xpath('//*[@id="arc_toolbar_report"]/div[1]/div[1]/div[1]/div/span')[0].text,  # 点赞数量
                      'coin': dom_tree.xpath('//*[@id="arc_toolbar_report"]/div[1]/div[1]/div[2]/div/span')[0].text,  # 投币数量
                      'star': dom_tree.xpath('//*[@id="arc_toolbar_report"]/div[1]/div[1]/div[3]/div/span')[0].text,  # 收藏数量
                      'share': dom_tree.xpath('//*[@class="video-share-info video-toolbar-item-text"]')[0].text,  # 分享数量
                      'tab': tab_list[rank-1]
                      }
    video_dic[bid] = video_dic_item
    rank += 1

# 视频列表中每个视频的时长
for key in video_dic.keys():
    x_path = '//*[@id="mirror-vdcon"]/div[2]/div/div[7]/div[1]/div[2]/div/div[1]/div['+str(video_dic[key]["rank"])+']/div/div[2]'
    long_text = dom_tree.xpath(x_path)[0].text
    video_dic[key]['long'] = str.strip(long_text)
# 写json,用的时候读json
json_str = json.dumps(video_dic)
with open('../basic.json', 'w') as file:
    file.write(json_str)

f = open("../basic.json", 'r')
content = f.read()
f.close()
video_dic = json.loads(content)
print(video_dic)
