import xmltodict
import csv

def xml_2_json(file_name:str):
    xml_file = open(file_name, 'r', encoding="UTF-8")
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
    return json_out, len(json_conversion)

def csv_2_json(file_name:str):
    csv_file = open(file_name, 'r', encoding="UTF-8")
    reader = csv.DictReader(csv_file)
    json_out = {'code': 1, 'data': []}
    len_danmu = 0
    for danmu in reader:
        one_danmaku = {"author": danmu['HASH'], "time": float(danmu['PROGRESS']), "text": danmu['TEXT'],
                       "color": danmu['COLOR'], "type": "scroll"}
        if danmu['MODE'] == '4':
            one_danmaku['type'] = "bottom"
        if danmu['MODE'] == '5':
            one_danmaku['type'] = "top"
        json_out['data'].append(one_danmaku)
        len_danmu += 1
    csv_file.close()
    # json_out['data'] = sorted(json_out['data'], key=lambda x: x['time'])
    return json_out, len_danmu
