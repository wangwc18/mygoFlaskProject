import json

from flask import Flask, render_template, request, send_file, redirect, url_for
import xmltodict

app = Flask(__name__)

mygo_data = {'Av914573114': {'rank': 1,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃1",
                             'play_time': '150.1万', 'danmaku_num': '9063', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:50", 'comment_num': 5670, 'load_danmaku': 3600,
                             'like': '5.3万', 'coin': '2.8万', 'star': '3.5万', 'share': '2.5万'
                             },
             'Av404602621': {'rank': 2,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃2",
                             'play_time': '30.1万', 'danmaku_num': '5624', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 638, 'load_danmaku': 3600,
                             'like': '9653', 'coin': '5086', 'star': '2388', 'share': '750'
                             },
             'Av404618862': {'rank': 3,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃3",
                             'play_time': '28.1万', 'danmaku_num': '5173', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 746, 'load_danmaku': 3600,
                             'like': '9897', 'coin': '5490', 'star': '2454', 'share': '415'
                             },
             'Av872091035': {'rank': 4,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃4",
                             'play_time': '23.4万', 'danmaku_num': '5562', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 266, 'load_danmaku': 3600,
                             'like': '6545', 'coin': '3634', 'star': '1624', 'share': '415'
                             },
             'Av659528201': {'rank': 5,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃5",
                             'play_time': '20.7万', 'danmaku_num': '4827', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 277, 'load_danmaku': 3600,
                             'like': '6263', 'coin': '3412', 'star': '1505', 'share': '354'
                             },
             'Av659536079': {'rank': 6,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃6",
                             'play_time': '19.9万', 'danmaku_num': '3886', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 262, 'load_danmaku': 3600,
                             'like': '5952', 'coin': '3357', 'star': '1439', 'share': '320'
                             },
             'Av447061316': {'rank': 7,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃7",
                             'play_time': '32.2万', 'danmaku_num': '6430', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 1014, 'load_danmaku': 3600,
                             'like': '9796', 'coin': '6394', 'star': '2332', 'share': '1146'
                             },
             'Av362022045': {'rank': 8,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃8",
                             'play_time': '37.6万', 'danmaku_num': '6454', 'upload_time': '2023-08-11 19:00:00',
                             'long': "23:40", 'comment_num': 2060, 'load_danmaku': 3600,
                             'like': '1.2万', 'coin': '5879', 'star': '2586', 'share': '1506'
                             },
             'Av232235089': {'rank': 9,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃9",
                             'play_time': '49.9万', 'danmaku_num': '7770', 'upload_time': '2023-08-13 22:49:03',
                             'long': "23:40", 'comment_num': 5079, 'load_danmaku': 3600,
                             'like': '1.9万', 'coin': '9793', 'star': '3723', 'share': '2318'
                             },
             'Av702479882': {'rank': 10,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃10",
                             'play_time': '71.0万', 'danmaku_num': '1.2万', 'upload_time': '2023-08-20 19:00:00',
                             'long': "23:40", 'comment_num': 5672, 'load_danmaku': 3600,
                             'like': '3.0万', 'coin': '2.3万', 'star': '7348', 'share': '4356'
                             },
             'Av275135823': {'rank': 11,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃11",
                             'play_time': '55.0万', 'danmaku_num': '1.0万', 'upload_time': '2023-08-27 19:00:00',
                             'long': "23:40", 'comment_num': 3278, 'load_danmaku': 3600,
                             'like': '2.5万', 'coin': '1.4万 ', 'star': '4692', 'share': '2459'
                             },
             'Av703057448': {'rank': 12,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃12",
                             'play_time': '51.6万', 'danmaku_num': '8875', 'upload_time': '2023-09-03 19:00:00',
                             'long': "23:40", 'comment_num': 4007, 'load_danmaku': 3600,
                             'like': '2.2万', 'coin': '1.4万', 'star': '4334', 'share': '2149'
                             },
             'Av618134604': {'rank': 13,
                             'title': "「BanG Dream! It's MyGO!!!!!」#1-#12 总集篇",
                             'play_time': '35.5万', 'danmaku_num': '5513', 'upload_time': '2023-09-07 21:30:00',
                             'long': "23:40", 'comment_num': 2234, 'load_danmaku': 3600,
                             'like': '1.5万', 'coin': '6202', 'star': '3568', 'share': '2545'
                             },
             'Av575884077': {'rank': 14,
                             'title': "「BanG Dream! It's MyGO!!!!!」＃13",
                             'play_time': '94.5万', 'danmaku_num': '2.4万', 'upload_time': '2023-09-14 21:35:00',
                             'long': "23:40", 'comment_num': 13494, 'load_danmaku': 3600,
                             'like': '4.3万', 'coin': '3.9万', 'star': '1.3万', 'share': '7674'
                             },
             }


@app.route('/video/<vid>')
def video_player(vid):
    if vid not in mygo_data.keys():
        return
    return render_template("main.html", vid=vid, videos=mygo_data)


@app.route('/')
def main_page():
    return redirect('/video/Av914573114')

@app.route('/mygo')
def mygo_page():
    vid = request.args.get("vid")
    if vid not in mygo_data.keys():
        vid = 'Av914573114'
    return render_template("mygo.html", vid=vid, videos=mygo_data)


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/api/comment')
def get_comment():
    vid = request.args.get("vid")
    rank = mygo_data[vid]['rank']
    cid = request.args.get("cid")
    page = request.args.get("page")
    if cid == '1':
        json_file = open('comment_hot_json/' + str(rank) + '/' + str(page) + '.json', 'r', encoding='UTF-8')
    elif cid == '2':
        json_file = open('comment_new_json/' + str(rank) + '/' + str(page) + '.json', 'r', encoding='UTF-8')
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
    return send_file('video\\' + str(rank) + '.mp4')


# @app.route("/api/danmu", methods=['GET'])
# def danmu_server():
#     vid = request.args.get("id")
#     if vid not in mygo_data.keys():
#         return
#     rank = mygo_data[vid]['rank']
#     xml_file = open('danmaku/' + str(rank) + '.xml', 'r', encoding="UTF-8")
#     parsed_data = xmltodict.parse(xml_file.read())
#     xml_file.close()
#     json_conversion = parsed_data['i']['d']
#     json_out = {'code': 1, 'danmaku': []}
#     for danmu in json_conversion:
#         list_param = danmu['@p'].split(',')
#         hex_color = hex(int(list_param[3]))[2:]
#         hex_color = '#' + '0' * (6 - len(hex_color)) + hex_color
#         one_danmaku = {"__v": 0, "author": list_param[6], "time": float(list_param[0]), "text": danmu['#text'],
#                        "color": hex_color, "type": "right"}
#         if list_param[1] == '4':
#             one_danmaku['type'] = "bottom"
#         if list_param[1] == '4':
#             one_danmaku['type'] = "top"
#         json_out['danmaku'].append(one_danmaku)
#     json_str = json.dumps(json_out, ensure_ascii=False)
#     headers = {"Content-Type": "application/json"}
#     return json_str, 200, headers


@app.route("/api/danmu", methods=['GET'])
def danmu_server():
    vid = request.args.get("id")
    if vid not in mygo_data.keys():
        return
    rank = mygo_data[vid]['rank']
    xml_file = open('danmaku/' + str(rank) + '.xml', 'r', encoding="UTF-8")
    parsed_data = xmltodict.parse(xml_file.read())
    xml_file.close()
    json_conversion = parsed_data['i']['d']
    json_out = {'code': 1, 'data': []}
    for danmu in json_conversion:
        list_param = danmu['@p'].split(',')
        hex_color = hex(int(list_param[3]))[2:]
        hex_color = '#' + '0' * (6 - len(hex_color)) + hex_color
        one_danmaku = {"author": list_param[6], "time": float(list_param[0]), "text": danmu['#text'],
                       "color": hex_color, "type": "scroll"}
        if list_param[1] == '4':
            one_danmaku['type'] = "bottom"
        if list_param[1] == '5':
            one_danmaku['type'] = "top"
        json_out['data'].append(one_danmaku)
    json_out['data'] = sorted(json_out['data'], key=lambda x: x['time'])
    json_str = json.dumps(json_out, ensure_ascii=False)
    headers = {"Content-Type": "application/json"}
    return json_str, 200, headers

# @app.route("/api/danmu", methods=['POST'])
# def danmu_post():
#     data = json.loads(request.get_data())
#     vid = data["player"]
#     if vid not in mygo_data.keys():
#         return
#     rank = mygo_data[vid]['rank']
#     xml_file = open('danmaku/' + str(rank) + '.xml', 'r', encoding="UTF-8")
#     parsed_data = xmltodict.parse(xml_file.read())
#     xml_file.close()
#     json_conversion = parsed_data['i']['d']
#     json_out = {'code': 1, 'danmaku': []}
#     for danmu in json_conversion:
#         list_param = danmu['@p'].split(',')
#         hex_color = hex(int(list_param[3]))[2:]
#         hex_color = '#' + '0' * (6 - len(hex_color)) + hex_color
#         one_danmaku = {"__v": 0, "author": list_param[6], "time": float(list_param[0]), "text": danmu['#text'],
#                        "color": hex_color, "type": "right"}
#         if list_param[1] == '4':
#             one_danmaku['type'] = "bottom"
#         if list_param[1] == '4':
#             one_danmaku['type'] = "top"
#         json_out['danmaku'].append(one_danmaku)
#     json_out['danmaku'].append({"__v": 0, "author": '1', "time": data["time"], "text": data["text"],
#                                 "color": data["color"], "type": data["type"]})
#     json_str = json.dumps(json_out, ensure_ascii=False)
#     headers = {"Content-Type": "application/json"}
#     return json_str, 200, headers


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
