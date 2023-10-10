import os
import requests


def download_image(image_url):
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
    dir_url = ''
    while i > 0:
        if file_url[i] == '/':
            dir_url = file_url[:i + 1]
            break
        i -= 1
    if not os.path.exists(dir_url):
        os.makedirs(dir_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    img_data = requests.get(url=image_url, headers=headers).content
    with open(file_url, 'wb') as f:
        f.write(img_data)


# dir_list=['13','sum01_12']
for dir in range(1, 15):
    out_put_dir = 'comment_json/' + str(dir) + '/'
    for file_json in os.listdir(out_put_dir):
        file_n = out_put_dir + file_json
        print(file_n)
        file = open(file_n, 'r', encoding='utf-8')
        json_str = file.read()
        file.close()
        index = len(json_str) - 1
        end = index
        is_now = False
        while (index > 7):
            if not is_now:
                if json_str[index - 3:index + 1] == '.jpg' \
                        or json_str[index - 3:index + 1] == '.png' or json_str[index - 3:index + 1] == '.webp' \
                        or json_str[index - 3:index + 1] == '.gif':
                    if '\u4e00' <= json_str[index - 4] <= '\u9fff' or json_str[index - 4] == '！' \
                            or json_str[index - 4] == 'び' or json_str[index - 4] == '？' or json_str[index - 4] == '”':
                        index -= 1
                        continue
                    end = index
                    is_now = True
            else:
                if json_str[index - 6:index + 1] == 'http://':
                    download_image(json_str[index - 6:end + 1])
                    is_now = False
                elif json_str[index - 7:index + 1] == 'https://':
                    download_image(json_str[index - 7:end + 1])
                    is_now = False
            index -= 1
