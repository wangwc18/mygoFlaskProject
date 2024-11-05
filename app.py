import json
from flask import Flask, render_template, request, send_file, redirect, url_for, make_response
from natsort import natsorted
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
from tools import xml_2_json, csv_2_json

app = Flask(__name__)

# 视频基本信息,懒事儿就不整数据库了
f = open("basic.json", 'r')
content = f.read()
f.close()
mygo_data = json.loads(content)
# 运行模式
f = open("run_mode.json", 'r')
content = f.read()
f.close()
run_mode = json.loads(content)['run_mode']
run_ip = json.loads(content)['ip']
run_port = json.loads(content)['port']
# 视频本地路径列表
mygo_video_list = []
for item in os.listdir('video/'):
    item_path = os.path.join('video/', item)
    if os.path.isfile(item_path):
        mygo_video_list.append(item_path)
mygo_video_list = natsorted(mygo_video_list)


@app.route('/video/<vid>')
def video_player(vid):
    if vid not in mygo_data.keys():
        return
    return render_template("main.html", vid=vid, videos=mygo_data)


@app.route('/')
def main_page():
    return redirect('/video/BV1Zu4y1B7DU')


@app.route('/mygo')
def mygo_page():
    vid = request.args.get("vid")
    if vid not in mygo_data.keys():
        vid = 'BV1Zu4y1B7DU'
    return render_template("mygo.html", vid=vid, videos=mygo_data)


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/api/comment')
def get_comment():
    vid = request.args.get("vid")  # 传入视频id
    rank = mygo_data[vid]['rank']  # 根据视频编号找到对应文件名
    cid = request.args.get("cid")  # cid=1为热评排序 cid=2为最新排序
    page = request.args.get("page")
    if cid == '1' and run_mode == 'outline':
        json_file = open('comment_hot_json/' + str(rank) + '/' + str(page) + '.json', 'r', encoding='UTF-8')
    elif cid == '1' and run_mode == 'online':
        json_file = open('comment_hot_json_online/' + str(rank) + '/' + str(page) + '.json', 'r', encoding='UTF-8')
    elif cid == '2' and run_mode == 'outline':
        json_file = open('comment_new_json/' + str(rank) + '/' + str(page) + '.json', 'r', encoding='UTF-8')
    elif cid == '2' and run_mode == 'online':
        json_file = open('comment_new_json_online/' + str(rank) + '/' + str(page) + '.json', 'r', encoding='UTF-8')
    else:
        return
    json_str = json_file.read()
    headers = {"Content-Type": "application/json"}
    json_file.close()
    return json_str, 200, headers


@app.route('/api/comment_more')
def get_comment_more():
    vid = request.args.get("vid")  # 传入视频id
    rank = mygo_data[vid]['rank']  # 根据视频编号找到对应文件名
    rpid = request.args.get("rpid")  # 评论id
    page = request.args.get("page")  # 页码
    if run_mode == 'outline':
        json_file = open('comment_more_json/' + str(rank) + '/' + str(rpid) + "_" + str(page) + '.json', 'r',
                         encoding='UTF-8')
    elif run_mode == 'online':
        json_file = open('comment_more_json_online/' + str(rank) + '/' + str(rpid) + "_" + str(page) + '.json', 'r',
                         encoding='UTF-8')
    else:
        return
    json_str = json_file.read()
    headers = {"Content-Type": "application/json"}
    json_file.close()
    return json_str, 200, headers


@app.route("/api/video")
def video_server():
    vid = request.args.get("vid")
    if vid not in mygo_data.keys():
        return
    rank = mygo_data[vid]['rank']
    return send_file(mygo_video_list[rank - 1])


@app.route("/api/danmu", methods=['GET'])
def danmu_server():
    vid = request.args.get("id")
    danmu_type = request.args.get("type")  # 弹幕类型
    if vid not in mygo_data.keys():
        return
    if danmu_type not in ['1', '2', '3']:  # 1:加载3600条标准弹幕 2:加载最多弹幕 3:加载早期弹幕
        danmu_type = '1'
    rank = mygo_data[vid]['rank']
    headers = {"Content-Type": "application/json"}
    if rank > 14:  # 没有特别篇的最多和开播数据，所以都用标准弹幕了
        file_name = 'danmaku/1/' + str(rank) + '.xml'
        json_out, len_danmu = xml_2_json(file_name)
    else:
        if danmu_type == '1':
            file_name = 'danmaku/1/' + str(rank) + '.xml'
            json_out, len_danmu = xml_2_json(file_name)
        elif danmu_type == '2':
            file_name = 'danmaku/2/ep' + str(rank) + '.csv'
            json_out, len_danmu = csv_2_json(file_name)
        else:
            file_name = 'danmaku/3/' + str(rank) + '.xml'
            json_out, len_danmu = xml_2_json(file_name)
    json_str = json.dumps(json_out, ensure_ascii=False)
    # mygo_data[vid]['load_danmaku'] = len_danmu
    return json_str, 200, headers


if __name__ == '__main__':
    app.run(host=run_ip, port=run_port)
