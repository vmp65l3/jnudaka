# -*- coding: utf-8 -*-

import requests
import json
import os

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
print(username)



HEADER = {
    'Host':'stuhealth.jnu.edu.cn',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept-Encoding':'gzip',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Origin':'https://stuhealth.jnu.edu.cn',
    'Referer':'https://stuhealth.jnu.edu.cn/',
}

def jnu_daka_login(login_info):
    print ("模拟登录中...")
    


    #login_data = json.dumps(login_info)
    
    response = requests.post(
        'https://stuhealth.jnu.edu.cn/api/user/login',
        data = login_info,
        headers = HEADER,
    )
    
    print(login_info)
    
    message = json.loads(response.content)
    if message['meta']['msg'] == '登录成功，今天已填写':
        return '您今天打过卡啦！'
    elif message['meta']['success'] == False:
        return '请检查你的抓包信息是否有误！'
    
    print('模拟打卡中...')
    

    # 获取 jnuid 和 idtype 
    jnuid = message['data']['jnuid']
    idtype = message['data']['idtype']

    # post stuinfo需要它们
    info_params = {
        'idType': idtype,
        'jnuid': jnuid
    }
    r = requests.post(
        'https://stuhealth.jnu.edu.cn/api/user/stuinfo',
        data=json.dumps(info_params),
        headers=HEADER
    )
    message = json.loads(r.content)

    # 学生姓名（你的
    name = message['data']['xm']

    # 构造打卡信息并上传
    # message['data']['mainTable']有你上一次打卡的信息
    # 可以利用它快速构造正确的信息
    mainData = message['data']['mainTable']
    health_params = {
        "mainTable":{
            "wayStart":mainData['wayStart'],
            "arriveTime":mainData['arriveTime'],
            "way2Start":mainData['way2Start'],
            "language":mainData['language'],
            "declareTime":message['meta']['timestamp'].split(' ')[0],
            "personNo":mainData['personNo'],
            "personName":message['data']['xm'],
            "sex":message['data']['xbm'],
            "professionName":message['data']['zy'],
            "collegeName":message['data']['yxsmc'],
            "phoneArea":mainData['phoneArea'],
            "phone":mainData['phone'],
            "assistantName":mainData['assistantName'],
            "assistantNo":mainData['assistantNo'],
            "className":mainData['className'],
            "linkman":mainData['linkman'],
            "linkmanPhoneArea":mainData['linkmanPhoneArea'],
            "linkmanPhone":mainData['linkmanPhone'],
            "personHealth":mainData['personHealth'],
            "temperature":mainData['temperature'],
            "personHealth2":mainData['personHealth2'],
            "leaveState":mainData['leaveState'],
            "leaveHubei":mainData['leaveHubei'],
            "wayType1":mainData['wayType1'],
            "wayType2":mainData['wayType2'],
            "wayType3":mainData['wayType3'],
            "wayType5":mainData['wayType5'],
            "wayType6":mainData['wayType6'],
            "wayTypeOther":mainData['wayTypeOther'],
            "wayNo":mainData['wayNo'],
            "currentArea":mainData['currentArea'],
            "inChina":mainData['inChina'],
            "personC1id":mainData['personC1id'],
            "personC1":mainData['personC1'],
            "personC2id":mainData['personC2id'],
            "personC2":mainData['personC2'],
            "personC3id":mainData['personC3id'],
            "personC3":mainData['personC3'],
            "personC4":mainData['personC4'],
            "otherC4":mainData['otherC4'],
            "isPass14C1":mainData['isPass14C1'],
            "isPass14C2":mainData['isPass14C2'],
            "isPass14C3":mainData['isPass14C3']
        },
        "jnuid":jnuid
    }

    r = requests.post(
        'https://stuhealth.jnu.edu.cn/api/write/main',
        data=json.dumps(health_params),
        headers=HEADER
    )
    message = json.loads(r.content)
    return name + '同学，' + '您于' + message['meta']['timestamp'] + ' 打卡成功！'
    

    
    

if __name__ == "__main__":
    login_info = {
        'username':username,
        'password':password,
    }
    print(login_info)
    print(jnu_daka_login(login_info))
   


