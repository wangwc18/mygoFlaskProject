import requests
import json

heads = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': """buvid3=61A3D6B6-EBAD-FC23-96AB-194DBB112A9D29721infoc; b_nut=1693960429; i-wanna-go-back=-1; b_ut=7; _uuid=B8C34697-A6EF-8C69-4BB10-A7D3AF38A61431685infoc; buvid4=4D72BDC2-D395-6C36-5669-332ED535AE9930928-023090608-cSrFUaBpzyFt3tKvmWMr%2Bg%3D%3D; home_feed_column=5; DedeUserID=125207414; DedeUserID__ckMd5=f63b6b886385a030; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(k|~RuR)R)~0J'uYmRJJk)lJ; buvid_fp_plain=undefined; LIVE_BUVID=AUTO2516944127685674; hit-new-style-dyn=1; hit-dyn-v2=1; CURRENT_QUALITY=80; SESSDATA=af3213bb%2C1711692561%2C12790%2Aa1CjAvUMfco_lqEBclJEMScS0nNbA1fAhhU9pEO6smXBlVv7vMO344T58JN8VVeADHV9USVjE0Qnp0alNrSC1mZmtSWUxjNlZuNTZCYlloZGpmQTNkWm1oNzlDa1czMjl6SjR3al92cFB1aDNaUFNjYjlqR2lpWWp1TS1YYnJnTzZmVlFBUFRlMEpBIIEC; bili_jct=8ab457173dd8900ba8ee120873175c57; fingerprint=2595ae963b0706333b23bf590ea83af4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTY0MTYxNDEsImlhdCI6MTY5NjE1Njg4MSwicGx0IjotMX0.C8vzREiqmqbe9X8H6YumaDP7HvlJF9_lRKcCl90UCMA; bili_ticket_expires=1696416081; browser_resolution=1920-923; b_lsid=F102D4EEF_18AEDFCC189; bp_video_offset_125207414=847612526044643333; sid=7mqwb4ho; PVID=2; buvid_fp=2595ae963b0706333b23bf590ea83af4""",
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

import hashlib
import time

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
    575884077]
kk = 1
for oid_int in oid_list:
    oid = str(oid_int)
    out_put_dir = 'comment_json_new/' + str(kk) + '/'
    kk += 1
    # all_num = int(647/20)+1
    # session_id = '1736852393199237'

    i = 'ea1db124af3c7062474693fa704f4ff8'

    wts = str(int(time.time()))
    f = 'mode=2&oid=' + oid + '&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts=' + wts
    input_str = f + i
    md5 = hashlib.md5()
    md5.update(input_str.encode('utf-8'))
    w_rid = md5.hexdigest()
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=2&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts

    html_content = requests.get(url, headers=heads).text
    file_n = out_put_dir + '1.json'
    file = open(file_n, 'w', encoding='utf-8')
    file.write(html_content)
    file.close()
    count = 2
    curse = json.loads(html_content)['data']['cursor']['pagination_reply']['next_offset']
    curse = json.loads(curse)['Data']['cursor']
    while curse > 0:
        wts = str(int(time.time()))
        f = 'mode=2&oid=' + oid + '&pagination_str=%7B%22offset%22%3A%22%7B%5C%22type%5C%22%3A3%2C%5C%22direction%5C%22%3A1%2C%5C%22Data%5C%22%3A%7B%5C%22cursor%5C%22%3A' + str(
            curse) + '%7D%7D%22%7D&plat=1&type=1&web_location=1315875&wts=' + wts
        input_str = f + i
        md5 = hashlib.md5()
        md5.update(input_str.encode('utf-8'))
        w_rid = md5.hexdigest()
        url = 'https://api.bilibili.com/x/v2/reply/wbi/main?oid=' + oid + '&type=1&mode=2&pagination_str=%7B%22offset%22:%22%7B%5C%22type%5C%22:3,%5C%22direction%5C%22:1,%5C%22Data%5C%22:%7B%5C%22cursor%5C%22:' + str(
            curse) + '%7D%7D%22%7D&plat=1&web_location=1315875&w_rid=' + w_rid + '&wts=' + wts
        html_content = requests.get(url, headers=heads).text
        if 'next_offset' not in json.loads(html_content)['data']['cursor']['pagination_reply']:
            break
        curse = json.loads(html_content)['data']['cursor']['pagination_reply']['next_offset']
        curse = json.loads(curse)['Data']
        if 'cursor' not in curse.keys():
            break
        else:
            curse = curse['cursor']
        # html_json=json.loads(html_content)
        file_n = out_put_dir + str(count) + '.json'
        file = open(file_n, 'w', encoding='utf-8')
        file.write(html_content)
        file.close()
        print(count, end=' ')
        count += 1

# wts = str(int(time.time()))
# f = 'mode=2&oid='+oid+'&pagination_str=%7B%22offset%22%3A%22%22%7D&plat=1&seek_rpid=&type=1&web_location=1315875&wts='+wts
# input_str = f+i
# md5 = hashlib.md5()
# md5.update(input_str.encode('utf-8'))
# w_rid = md5.hexdigest()
# url ='https://api.bilibili.com/x/v2/reply/wbi/main?oid='+oid+'&type=1&mode=2&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid='+w_rid+'&wts='+wts
# html_content = requests.get(url, headers=heads).text
# file_n = out_put_dir+'1.json'
# file = open(file_n,'w',encoding='utf-8')
# file.write(html_content)
# file.close()
