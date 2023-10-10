import os
import json
import datetime

def http_str_to_static(http_str):
    if http_str is None or http_str=='':
        return http_str
    if http_str[:7]=='http://':
        return '/static/pic/'+http_str[7:]
    if http_str[:8]=='https://':
        return '/static/pic/'+http_str[8:]
    return http_str

def json_n_to_html_br(json_n):
    if json_n is None or json_n=='':
        return json_n
    return json_n.replace('\n','<br>')

def unix_time_to_date(unix_time):
    date = datetime.datetime.fromtimestamp(unix_time)
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

for i in range(1,15):
    dir_path='comment_json/'+str(i)+"/"
    comment_in_one = []
    top_comment_in_one = []
    for file_path in os.listdir(dir_path):
        json_path=dir_path+file_path
        print(json_path)
        json_file = open(json_path, 'r', encoding='UTF-8')
        json_str = json_file.read()
        json_file.close()
        data_dir = json.loads(json_str)['data']
        json_out = {'errno': 0, 'totalPage': len(os.listdir(dir_path)), 'replies': [],'top_replies':[]}
        for comment in data_dir['replies']:
            json_comment = {
                'avatar': http_str_to_static(comment['member']['avatar']),
                'pendant': http_str_to_static(comment['member']['pendant']['image']),
                'uname': comment['member']['uname'],
                'current_level': comment['member']['level_info']['current_level'],
                'vipStatus': comment['member']['vip']['vipStatus'],
                'is_senior_member': comment['member']['is_senior_member'],
                'user_sailing': '',
                'message': json_n_to_html_br(comment['content']['message']),
                'ctime': unix_time_to_date(comment['ctime']),
                'like': comment['like'],
                'replies': [],
                'sub_reply_entry_text': "",
                'pictures': [],
            }
            if 'pictures' in comment['content'].keys():
                for pic_num in range(len(comment['content']['pictures'])):
                    comment['content']['pictures'][pic_num]['img_src']=http_str_to_static(comment['content']['pictures'][pic_num]['img_src'])
                json_comment['pictures'] = comment['content']['pictures']

            if 'user_sailing' in comment['member'].keys():
                if comment['member']['user_sailing'] is not None \
                        and 'cardbg' in comment['member']['user_sailing'].keys() \
                        and comment['member']['user_sailing']['cardbg'] is not None \
                        and comment['member']['user_sailing']['cardbg']['image'] is not None:
                    comment['member']['user_sailing']['cardbg']['image']= http_str_to_static(comment['member']['user_sailing']['cardbg']['image'])
                    json_comment['user_sailing'] = comment['member']['user_sailing']['cardbg']

                # print(i,file_path,comment['content']['message'])
            if 'sub_reply_entry_text' in comment['reply_control'].keys():
                json_comment['sub_reply_entry_text']=comment['reply_control']['sub_reply_entry_text']
            if comment['replies'] is not None:
                for reply in comment['replies']:
                    json_reply = {
                        'avatar': http_str_to_static(reply['member']['avatar']),
                        'uname': reply['member']['uname'],
                        'current_level': reply['member']['level_info']['current_level'],
                        'vipStatus': reply['member']['vip']['vipStatus'],
                        'is_senior_member': reply['member']['is_senior_member'],
                        'message': json_n_to_html_br(reply['content']['message']),
                        'ctime': unix_time_to_date(reply['ctime']),
                        'like': reply['like'],
                    }
                    json_comment['replies'].append(json_reply)
            json_out['replies'].append(json_comment)
            comment_in_one = comment_in_one + [json_comment] ###########

        if 'top_replies' not in data_dir.keys() or data_dir['top_replies'] is None:
            continue
        for top_comment in data_dir['top_replies']:
            json_comment = {
                'avatar': http_str_to_static(top_comment['member']['avatar']),
                'pendant': http_str_to_static(top_comment['member']['pendant']['image']),
                'uname': top_comment['member']['uname'],
                'current_level': top_comment['member']['level_info']['current_level'],
                'vipStatus': top_comment['member']['vip']['vipStatus'],
                'is_senior_member': top_comment['member']['is_senior_member'],
                'user_sailing': '',
                'message': json_n_to_html_br(top_comment['content']['message']),
                'ctime': unix_time_to_date(top_comment['ctime']),
                'like': top_comment['like'],
                'replies': [],
                'sub_reply_entry_text': "",
                 'pictures': [],
            }
            if 'pictures' in top_comment['content'].keys():
                json_comment['pictures']=top_comment['content']['pictures']
                print("youyouyou")

            if 'user_sailing' in top_comment['member'].keys():
                if top_comment['member']['user_sailing'] is not None \
                        and 'cardbg' in top_comment['member']['user_sailing'].keys() \
                        and top_comment['member']['user_sailing']['cardbg'] is not None \
                        and top_comment['member']['user_sailing']['cardbg']['image'] is not None:
                    top_comment['member']['user_sailing']['cardbg']['image'] = http_str_to_static(
                        top_comment['member']['user_sailing']['cardbg']['image'])
                    json_comment['user_sailing'] = top_comment['member']['user_sailing']['cardbg']

            if 'sub_reply_entry_text' in top_comment['reply_control'].keys():
                json_comment['sub_reply_entry_text']=top_comment['reply_control']['sub_reply_entry_text']
            if top_comment['replies'] is not None:
                for top_reply in top_comment['replies']:
                    json_reply = {
                        'avatar': http_str_to_static(top_reply['member']['avatar']),
                        'uname': top_reply['member']['uname'],
                        'current_level': top_reply['member']['level_info']['current_level'],
                        'vipStatus': top_reply['member']['vip']['vipStatus'],
                        'is_senior_member': top_reply['member']['is_senior_member'],
                        'message': json_n_to_html_br(top_reply['content']['message']),
                        'ctime': unix_time_to_date(top_reply['ctime']),
                        'like': top_reply['like'],
                    }
                    json_comment['replies'].append(json_reply)
            json_out['top_replies'].append(json_comment)
            top_comment_in_one = top_comment_in_one + [json_comment] ##############


        json_str = json.dumps(json_out, ensure_ascii=False)
        out_dir='../comment_hot_json/'+str(i)+"/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        json_file = open(out_dir+file_path, 'w', encoding='UTF-8')
        json_file.write(json_str)
        json_file.close()

    comment_in_one.sort(key=lambda x: x['ctime'], reverse=True)
    top_comment_in_one.sort(key=lambda x: x['ctime'],reverse=True)
    top_comment_in_one=top_comment_in_one[0:1]
    if len(comment_in_one)%20==0:
        totalPage = int(len(comment_in_one)/20)
    else:
        totalPage = int(len(comment_in_one) / 20)+1
    new_page=1
    for k in range(0, len(comment_in_one), 20):
        if (k+20)>len(comment_in_one):
            end=len(comment_in_one)
        else:
            end=k+20
        if k==0:
            json_new_out = {'errno': 0, 'totalPage': totalPage, 'replies': comment_in_one[k:end], 'top_replies': top_comment_in_one}
        else:
            json_new_out = {'errno': 0, 'totalPage': totalPage, 'replies': comment_in_one[k:end],'top_replies': []}
        json_new_out = json.dumps(json_new_out, ensure_ascii=False)
        out_dir = '../comment_new_json/' + str(i) + "/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        json_file = open(out_dir + str(new_page)+".json", 'w', encoding='UTF-8')
        json_file.write(json_new_out)
        json_file.close()
        new_page+=1