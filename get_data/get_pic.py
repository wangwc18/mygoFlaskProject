import json
import os
import requests

"""
评论区图片爬取
"""

def download_image(image_url):
    """
    下载单张图片
    :param image_url: 图片url
    :return:
    """
    if image_url is None or image_url == '':
        return
    file_url = ''
    if image_url[:5] == 'http:':
        file_url = image_url[7:]
    else:
        file_url = image_url[8:]
    # file_url = file_url[:18].replace('.', '_') + file_url[18:]
    file_url = '../static/pic/' + file_url
    if os.path.exists(file_url):
        return
    i = len(file_url) - 5
    dir_url = ''  # 要拼出图片所在目录
    while i > 0:
        if file_url[i] == '/':  # 从后向前找直到找出‘/’，‘/’以前就是目录名
            dir_url = file_url[:i + 1]
            break
        i -= 1
    if not os.path.exists(dir_url):  # 图片所在目录不存在就新建
        os.makedirs(dir_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    img_data = requests.get(url=image_url, headers=headers).content
    print(file_url)
    with open(file_url, 'wb') as f:
        f.write(img_data)


def download_reply_img(reply_list: list):
    """
    json解析出的评论列表相关图片下载
    :param reply_list: 评论列表
    :return:
    """
    for comment in reply_list:
        download_image(comment['member']['avatar'])  # 头像(转本地图片链接)
        download_image(comment['member']['pendant']['image'])  # 头像框(转本地图片链接)
        # 处理评论里头的图片
        if 'pictures' in comment['content'].keys():
            for pic_num in range(len(comment['content']['pictures'])):
                download_image(comment['content']['pictures'][pic_num]['img_src'])
        # 处理右侧徽章字典
        if 'user_sailing' in comment['member'].keys():
            if comment['member']['user_sailing'] is not None \
                    and 'cardbg' in comment['member']['user_sailing'].keys() \
                    and comment['member']['user_sailing']['cardbg'] is not None \
                    and comment['member']['user_sailing']['cardbg']['image'] is not None:
                # 处理徽章图片
                download_image(comment['member']['user_sailing']['cardbg']['image'])
            download_reply_reply_img(comment['replies'])


def download_reply_reply_img(reply_reply_list: list) -> list:
    """
    json解析出的评论回复相关图片下载
    :param reply_reply_list: 评论回复列表
    :return:
    """
    for reply in reply_reply_list:
        download_image(reply['member']['avatar'])  # 回复只有头像图片(转本地图片链接)


def download_page_img(input_dir: str, file_path: str):
    """
    下载“最热/最新评论”json文件中的图片
    :param input_dir: json文件所在路径 xxx/xxx/
    :param file_path: json文件名，1.json
    :return:
    """
    json_path = input_dir + file_path
    json_file = open(json_path, 'r', encoding='UTF-8')
    json_str = json_file.read()
    json_file.close()
    data_dir = json.loads(json_str)['data']
    download_reply_img(data_dir['replies'])
    if file_path == '1.json':  # 只有第一页包含置顶评论，下载置顶评论相关图片
        download_reply_img(data_dir['top_replies'])


def download_more_img(input_dir: str, file_path: str):
    """
    下载“回复评论”json文件中的图片
    :param input_dir:
    :param file_path:
    :return:
    """
    json_path = input_dir + file_path
    json_file = open(json_path, 'r', encoding='UTF-8')
    json_str = json_file.read()
    json_file.close()
    data_dir = json.loads(json_str)['data']
    download_reply_reply_img(data_dir['replies'])


for i in range(1, 17):
    # 处理最热评论
    dir_path = 'comment_json_hot/'+str(i)+"/"
    for file_path in os.listdir(dir_path):
        download_page_img(dir_path, file_path)
        print(dir_path+file_path)
    # 处理最新评论
    dir_path = 'comment_json_new/' + str(i) + "/"
    for file_path in os.listdir(dir_path):
        download_page_img(dir_path, file_path)
        print(dir_path + file_path)
    # 处理更多评论
    dir_path = 'comment_json_more/' + str(i) + "/"
    for file_path in os.listdir(dir_path):
        download_more_img(dir_path, file_path)
        print(dir_path + file_path)


