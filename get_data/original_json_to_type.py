import os
import json
import datetime

"""
通过get_comment.py爬取的原始json原始数据太多了，
我们的页面没这么复杂精简一下，这样处理会快一点
"""


def http_str_to_static(http_str: str, output_type: str):
    """
    把b站图片资源url变到本地资源url
    :param http_str:
    :param output_type: online:输出原来的链接 outline:输出本地链接
    :return:
    """
    if http_str is None or http_str == '' or output_type == "online":
        return http_str
    if http_str[:7] == 'http://':
        return '/static/pic/' + http_str[7:]
    if http_str[:8] == 'https://':
        return '/static/pic/' + http_str[8:]
    return http_str


def json_n_to_html_br(json_n):
    """
    评论区如果有换行符\n对于html不生效，所以要转为html的换行符<br>
    :param json_n:
    :return:
    """
    if json_n is None or json_n == '':
        return json_n
    return json_n.replace('\n', '<br>')


def unix_time_to_date(unix_time):
    """
    unix时间戳转成%Y-%m-%d %H:%M:%S字符串
    :param unix_time:
    :return:
    """
    date = datetime.datetime.fromtimestamp(unix_time)
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def simplify_reply_json(reply_list: list, output_type: str) -> list:
    """
    把json中的评论列表简化
    :param reply_list: 评论列表
    :param output_type: online:输出原来的链接 outline:输出本地链接
    :return: 简化评论列表
    """
    replies = []
    for comment in reply_list:
        json_comment = {
            'rpid': comment['rpid'],  # 该条评论的id(int)
            'avatar': http_str_to_static(comment['member']['avatar'],output_type),  # 头像(转本地图片链接)
            'pendant': http_str_to_static(comment['member']['pendant']['image'],output_type),  # 头像框(转本地图片链接)
            'uname': comment['member']['uname'],  # 用户名
            'current_level': comment['member']['level_info']['current_level'],  # 用户等级1-6
            'vipStatus': comment['member']['vip']['vipStatus'],  # 是否大会员 0/1
            'is_senior_member': comment['member']['is_senior_member'],  # 是否高级会员lv6+ 0/1
            'fans_detail': '',  # 粉丝标签（迷子n级）
            'user_sailing': '',  # 右侧徽章字典
            'message': json_n_to_html_br(comment['content']['message']),  # 评论内容
            'ctime': unix_time_to_date(comment['ctime']),  # 评论时间(unix时间转格式 )
            'like': comment['like'],  # 该条评论点赞数量
            'pictures': [],  # 评论的图片链接列表(一般是笔记)
            'replies': [],  # 评论的回复列表字典
            'sub_reply_entry_text': "",  # 没有展示完的回复信息，如“共13条回复”
            'rcount':comment['rcount'],  # 回复数量
        }
        # 处理评论里头的图片
        if 'pictures' in comment['content'].keys():
            for pic_num in range(len(comment['content']['pictures'])):
                comment['content']['pictures'][pic_num]['img_src'] = http_str_to_static(
                    comment['content']['pictures'][pic_num]['img_src'],output_type)
            json_comment['pictures'] = comment['content']['pictures']
        # 处理右侧徽章字典
        if 'user_sailing' in comment['member'].keys():
            if comment['member']['user_sailing'] is not None \
                    and 'cardbg' in comment['member']['user_sailing'].keys() \
                    and comment['member']['user_sailing']['cardbg'] is not None \
                    and comment['member']['user_sailing']['cardbg']['image'] is not None:
                # 处理徽章图片
                comment['member']['user_sailing']['cardbg']['image'] = http_str_to_static(
                    comment['member']['user_sailing']['cardbg']['image'],output_type)
                # 整个赋值
                json_comment['user_sailing'] = comment['member']['user_sailing']['cardbg']
        # 处理粉丝标签（迷子n级）
        if 'fans_detail' in comment['member'].keys():
            if comment['member']['fans_detail'] is not None \
                    and 'medal_name' in comment['member']['fans_detail'].keys() \
                    and comment['member']['fans_detail']['medal_name'] is not None \
                    and comment['member']['fans_detail']['level'] is not None:
                # 整个赋值
                json_comment['fans_detail'] = comment['member']['fans_detail']
        # 没有展示完的回复信息
        if 'sub_reply_entry_text' in comment['reply_control'].keys():
            json_comment['sub_reply_entry_text'] = comment['reply_control']['sub_reply_entry_text']
        # 处理回复
        if comment['replies'] is not None:
            json_comment['replies'] = simplify_reply_reply_json(comment['replies'],output_type)
        replies.append(json_comment)
    return replies


def simplify_reply_reply_json(reply_reply_list: list, output_type: str) -> list:
    """
    把json中的评论的回复列表简化
    :param reply_reply_list: 评论回复列表
    :param output_type: online:输出原来的链接 outline:输出本地链接
    :return: 简化的评论回复列表
    """
    replies = []
    for reply in reply_reply_list:
        json_reply = {
            'avatar': http_str_to_static(reply['member']['avatar'], output_type),  # 回复头像（回复里没有头像框）
            'uname': reply['member']['uname'],  # 回复人名称
            'current_level': reply['member']['level_info']['current_level'],  # 回复人等级
            'vipStatus': reply['member']['vip']['vipStatus'],  # 回复人是否大会员
            'is_senior_member': reply['member']['is_senior_member'],  # 回复人是否lv6+
            'message': json_n_to_html_br(reply['content']['message']),  # 回复内容(回复@的信息也在里面)
            'ctime': unix_time_to_date(reply['ctime']),  # 回复时间
            'like': reply['like'],  # 回复点赞数量
        }
        replies.append(json_reply)
    return replies


def convert_page_json(input_dir: str, file_path: str, ouput_dir: str, output_type: str):
    """
    把评论页面json简化后输出到新文件夹
    :param input_dir: 输入路径 xxx/xxx/
    :param file_path: 输入文件名 1.json 可以拼出输入路径xxx/xxx/1.json
    :param ouput_dir: 输出路径 yyy/yyy/ 可以拼出输入路径yyy/yyy/1.json
    :param output_type: online:输出原来的链接 outline:输出本地链接
    :return:
    """
    json_path = input_dir + file_path
    json_file = open(json_path, 'r', encoding='UTF-8')
    json_str = json_file.read()
    json_file.close()
    data_dir = json.loads(json_str)['data']
    json_out = {'errno': 0, 'totalPage': len(os.listdir(input_dir)), 'all_count': data_dir['cursor']['all_count'],
                'replies': simplify_reply_json(data_dir['replies'], output_type), 'top_replies': []}
    if file_path == '1.json':  # 只有第一页包含置顶评论
        json_out['top_replies'] = simplify_reply_json(data_dir['top_replies'],output_type)
    # 处理完毕，写入json
    json_str = json.dumps(json_out, ensure_ascii=False)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    json_file = open(ouput_dir + file_path, 'w', encoding='UTF-8')
    json_file.write(json_str)
    json_file.close()


def convert_more_json(input_dir: str, file_path: str, ouput_dir: str, output_type: str):
    """
    把”评论回复更多“json简化后输出到新文件夹
    :param input_dir: 输入路径 xxx/xxx/
    :param file_path: 输入文件名 1.json 可以拼出输入路径xxx/xxx/1.json
    :param ouput_dir: 输出路径 yyy/yyy/ 可以拼出输入路径yyy/yyy/1.json
    :param output_type: online:输出原来的链接 outline:输出本地链接
    :return:
    """
    json_path = input_dir + file_path
    json_file = open(json_path, 'r', encoding='UTF-8')
    json_str = json_file.read()
    json_file.close()
    data_dir = json.loads(json_str)['data']
    json_out = {'errno': 0, 'totalPage': data_dir['page']['count'], 'replies': []}
    json_out['replies'] = simplify_reply_reply_json(data_dir['replies'], output_type)
    # 处理完毕，写入json
    json_str = json.dumps(json_out, ensure_ascii=False)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    json_file = open(ouput_dir + file_path, 'w', encoding='UTF-8')
    json_file.write(json_str)
    json_file.close()


output_type_list = ['online', 'outline']
for i in range(1, 17):
    for output_type in output_type_list:
        # 处理最热评论
        dir_path = 'comment_json_hot/' + str(i) + "/"
        out_dir = '../comment_hot_json/' + str(i) + "/" if output_type == 'outline' else '../comment_hot_json_online/' + str(i) + "/"
        for file_path in os.listdir(dir_path):
            convert_page_json(dir_path, file_path, out_dir, output_type)
            print(out_dir + file_path)
        # 处理最新评论
        dir_path = 'comment_json_new/' + str(i) + "/"
        out_dir = '../comment_new_json/' + str(i) + "/" if output_type == 'outline' else '../comment_new_json_online/' + str(i) + "/"
        for file_path in os.listdir(dir_path):
            convert_page_json(dir_path, file_path, out_dir, output_type)
            print(out_dir + file_path)
        # 处理更多评论
        dir_path = 'comment_json_more/' + str(i) + "/"
        out_dir = '../comment_more_json/' + str(i) + "/" if output_type == 'outline' else '../comment_more_json_online/' + str(i) + "/"
        for file_path in os.listdir(dir_path):
            convert_more_json(dir_path, file_path, out_dir, output_type)
            print(out_dir + file_path)
