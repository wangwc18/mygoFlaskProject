import math
import requests
import json
import os
import hashlib
import time

"""
获取所有评论以及回复
最热评论:comment_json_hot/ 
最新评论:comment_json_new/ 
更多评论:comment_json_more/
b站的反爬：先把(所有参数+unix时间)拼到一起，之后用md5做hash摘要，之后用(所有参数+unix时间+摘要值)去请求，
还好这个摘要算法不是自己写的，要不这里还得找出具体执行了哪些js
"""

# 请求头里的cookie会过期，爬之前先替换掉
heads = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': """""",
    'Origin': 'https://www.bilibili.com',
    'Referer': 'https://www.bilibili.com/video/BV1Zu4y1B7DU/?spm_id_from=333.788&vd_source=19b47bce4d7430571a27ab58f7085e08',
    'Sec-Ch-Ua': '''"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"''',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
wt = ''  # comment-pc-vue.next.js源码中“const Wt = getPictureHashKey(Vt + Zt)”运算值，替换成自己的


def save_by_name(content: str, output_dir: str):
    """
    把content输入文件,路径为output_dir
    :param content: 文件内容
    :param output_dir: 文件路径
    :return:
    """
    file = open(output_dir, 'w', encoding='utf-8')
    file.write(content)
    file.close()


def md5_hash(input_str: str) -> str:
    """
    md5哈希摘要
    :param input_str: 输入字符串
    :return: 摘要值
    """
    md5 = hashlib.md5()
    md5.update(input_str.encode('utf-8'))
    return md5.hexdigest()


def get_save_one_comment_more(oid: str, rpid: str, rcount: int, output_dir: str):
    """
    根据 视频oid的评论rpid,爬取保存这个评论的所有”更多回复“
    :param oid: ibilibili.com中的AID
    :param rpid: 评论id
    :param rcount: 评论的回复数量
    :param output_dir: ”更多回复“输出路径
    :return:
    """
    page = math.ceil(rcount * 1.0 / 10.0)
    rpid = str(rpid)
    print(rpid, end='更多回复 ')
    for i in range(1, page + 1):
        wts = str(int(time.time()))
        jt = 'gaia_source=main_web&oid=' + oid + '&pn=' + str(
            i) + '&ps=10&root=180345138432&type=1&web_location=333.788&wts=' + wts
        w_rid = md5_hash(jt + wt)
        url = 'https://api.bilibili.com/x/v2/reply/reply?oid=' + oid + '&type=1&root=' + rpid + '&ps=10&pn=' + str(
            i) + '&gaia_source=main_web&web_location=333.788&w_rid=' + w_rid + '&wts=' + wts
        html_content = requests.get(url, headers=heads).text
        file_n = output_dir + rpid + '_' + str(i) + '.json'
        save_by_name(html_content, file_n)
        print(i, end=' ')
    print()


def get_more_comment_list(replies_list: list) -> list:
    """
    根据json中replies列表，分析哪些评论是有"更多评论的"
    :param replies_list: json中replies列表
    :return: 评论id和回复条数列表 [(rpid1,rcount1),(rpid2,rcount2)....]
    """
    result_list = []
    for reply in replies_list:
        if len(reply['replies']) < reply['rcount']:  # 显示回复条数少于实际回复条数
            result_list.append((reply['rpid'], reply['rcount']))
    return result_list


def get_save_one_video_comment(oid: str, wt: str, comment_type: str, out_put_dir: str, more_dir: dir,
                               contain_more: bool):
    """
    获取一个oid视频的所有评论
    :param oid: ibilibili.com中的AID
    :param wt: 源码中“const Wt = getPictureHashKey(Vt + Zt)”运算值
    :param comment_type: hot/new 爬取最热/最新视频
    :param out_put_dir: 评论输出路径，xxx/xxx/
    :param more_dir: 更多评论输出路径，xxx/xxx/
    :param contain_more: 是否爬取“更多”中的评论
    :return:
    """
    # 爬第一屏评论区
    wts = str(int(time.time()))  # unix时间
    if comment_type == 'hot':
        jt = 'mode=3&oid=' + oid + '&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts=' + wts
    else:
        jt = 'mode=2&oid=' + oid + '&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts=' + wts
    w_rid = md5_hash(jt + wt)  # (所有参数+时间)做md5摘要
    if comment_type == 'hot':
        url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts
    else:
        url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=2&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts
    html_content = requests.get(url, headers=heads).text
    save_by_name(html_content, out_put_dir + '1.json')  # 返回json原封不动写入文件待进一步处理
    print('1', "屏评论")
    # 第一屏是否存在后继判定字段判断
    if comment_type == 'hot':
        # 热门评论在第一屏获取后得到session_id,之后的内容带着session_id重复获取，直到is_end为True
        session_id = json.loads(html_content)['data']['cursor']['session_id']
        if str(json.loads(html_content)['data']['cursor']['is_end']) == 'True':
            curse = 0
        else:
            curse = 1
    else:
        # 最新评论的结束字段在curse中，curse>0 则后面还有内容
        curse = json.loads(html_content)['data']['cursor']['pagination_reply']['next_offset']
        curse = json.loads(curse)['Data']['cursor']
    if contain_more:
        top_reply_list = get_more_comment_list(json.loads(html_content)['data']['top_replies'])
        reply_list = top_reply_list + get_more_comment_list(json.loads(html_content)['data']['replies'])
        for rpid, rcount in reply_list:
            get_save_one_comment_more(oid, rpid, rcount, more_dir)
    # 存在2、3、4。。。。屏评论，继续爬取
    count = 2  # 后面从第二页开始
    while curse > 0:
        # 原理同第一页，但是参数有所不同
        wts = str(int(time.time()))
        if comment_type == 'hot':
            jt = "mode=3&oid=" + oid + "&pagination_str=%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A1%2C%5C%22direction%5C%22%3A1%2C%5C%22session_id%5C%22%3A%5C%22" + session_id + "%5C%22%2C%5C%22data%5C%22%3A%7B%7D%7D%22%7D&plat=1&type=1&web_location=1315875&wts=" + wts
        else:
            jt = 'mode=2&oid=' + oid + '&pagination_str=%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A3%2C%5C%22direction%5C%22%3A1%2C%5C%22Data%5C%22%3A%7B%5C%22cursor%5C%22%3A' + str(
                curse) + '%7D%7D%22%7D&plat=1&type=1&web_location=1315875&wts=' + wts
        w_rid = md5_hash(jt + wt)
        if comment_type == 'hot':
            url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=3&pagination_str=%7B%22offset%22:%22%7B%5C%22type%5C%22:1,%5C%22direction%5C%22:1,%5C%22session_id%5C%22:%5C%22' + session_id + '%5C%22,%5C%22data%5C%22:%7B%7D%7D%22%7D&plat=1&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts
        else:
            url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=2&pagination_str=%7B%22offset%22:%22%7B%5C%22type%5C%22:3,%5C%22direction%5C%22:1,%5C%22Data%5C%22:%7B%5C%22cursor%5C%22:' + str(
                curse) + '%7D%7D%22%7D&plat=1&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts
        html_content = requests.get(url, headers=heads).text
        # 爬取更多评论
        if contain_more:
            reply_list = get_more_comment_list(json.loads(html_content)['data']['replies'])  # 后续页不怕取置顶评论的“更多评论”
            for rpid, rcount in reply_list:
                get_save_one_comment_more(oid, rpid, rcount, more_dir)
        # 后续页终止条件判断
        if comment_type == 'hot':
            if str(json.loads(html_content)['data']['cursor']['is_end']) == 'True':
                save_by_name(html_content, out_put_dir + str(count) + '.json')
                print(count, end=' ')
                break
        else:
            curse = json.loads(html_content)['data']['cursor']['pagination_reply']['next_offset']
            curse = json.loads(curse)['Data']
            if 'next' not in json.loads(html_content)['data']['cursor'].keys() or curse==0:
                break
            else:
                curse = curse['cursor']
        save_by_name(html_content, out_put_dir + str(count) + '.json')
        print(count, "屏评论")
        count += 1

# 爬取视频的oid列表:https://www.ibilibili.com/video/BV1Zu4y1B7DU里的AID
oid_list = [
    914573114,
    404602621,
    404618862,
    872091035,
    659528201,
    659536079,
    447061316,
    362022045,
    232235089,
    702479882,
    275135823,
    703057448,
    618134604,
    575884077,
    746164683,
    874056245,
]
oid_list = list(reversed(oid_list))  # 倒序爬取，感觉下架前大家都是在第一条视频下评论
type_list = ['hot', 'new']  # 先爬最热评论再爬最新
output_dir_list = ['comment_json_hot/', 'comment_json_new/', 'comment_json_more/']
for output_dir in output_dir_list:  # 新建输出目录
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
kk = len(oid_list)  # 输出目录序号，也是倒序的
for oid_int in oid_list:
    for comment_type in type_list:
        oid = str(oid_int)
        # 最热评论:comment_json_hot/ 最新评论:comment_json_new/ 更多评论:comment_json_more/
        if comment_type == 'hot':
            out_put_dir = output_dir_list[0] + str(kk) + '/'
        else:
            out_put_dir = output_dir_list[1] + str(kk) + '/'
        more_dir = output_dir_list[2] + str(kk) + '/'
        # 输出目录不存在就新建
        if not os.path.exists(out_put_dir):
            os.mkdir(out_put_dir)
        if not os.path.exists(more_dir):
            os.mkdir(more_dir)
        print("---------爬取第" + str(kk) + "个视频" + comment_type + "评论---------")
        # 在爬取最热评论时同时爬取”更多评论“，”更多评论”内容对于最热和最新是一样的
        get_save_one_video_comment(oid, wt, comment_type, out_put_dir, more_dir, comment_type == "hot")
    kk -= 1
