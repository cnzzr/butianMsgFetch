# -*- encoding:utf-8 -*-
import os

import requests
import json
import time
from configparser import ConfigParser

real_path = os.path.split(os.path.realpath(__file__))
ConfigFileName = os.path.join(real_path[0],'butian.cfg')
# 生成config对象
global_config = ConfigParser()
# 用config对象读取配置文件
global_config.read(ConfigFileName)
# 指定section，option读取值
cookie = global_config.get("butian", "cookie")
lastMsgId = global_config.getint("butian", "lastMsgId")

headers = {
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Origin": "https://www.butian.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.butian.net/Message",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": cookie
}

butianApi = "https://www.butian.net/Home/Message/lists"
butianApiSpace = "https://www.butian.net/WhiteHat/Center/spaceData"


def send_wechat(gconfig, message):
    """推送信息到微信"""
    url = 'https://push.bot.qw360.cn/send/{}'.format(gconfig.get('messenger', 'server_chan_sckey'))
    payload = {
        "msg": message
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    resp = requests.post(url, json=payload, headers=headers)
    print(resp.text)


def queryRank(gconfig, token, notice=False):
    ''' 获取白帽子信息：排名、积分、漏洞数
    '''
    rankOld = gconfig.getint("butian", "rank")
    response = requests.post(butianApiSpace, data={"token": token}, headers=headers)
    responseContent = str(response.content, "utf-8")
    spaceDataJson = json.loads(responseContent)
    if msgJson.get("status") != 1:
        return None
    rank = spaceDataJson.get("data").get("rank")
    extcredits = spaceDataJson.get("data").get("extcredits")
    loo_count = spaceDataJson.get("data").get("loo_count")
    if rankOld != rank and notice:
        # 发送提醒
        msg = "排名 {} , 积分 {} , 漏洞 {}".format(str(rank), str(extcredits), str(loo_count))
        send_wechat(global_config, msg)
    return rank


params = {
    "ajax": 1,
    "id": 0,
    "status": -1,
    "page": 1
}
try:
    response = requests.post(butianApi, data=params, headers=headers)
except Exception as ex:
    time.sleep(1)
    response = requests.post(butianApi, data=params, headers=headers, timeout=(30, 60))

responseContent = str(response.content, "utf-8")
msgJson = json.loads(responseContent)

'''
{status: 1, info: "success",…}
    data: {list: [{id: "2457501", title: "您所提交的漏洞XX登录地址存在可撞库的风险未通过审核", content: "", type: "漏洞消息",…},…],…}
    count: "12"
    list: [{id: "2457501", title: "您所提交的漏洞XX登录地址存在可撞库的风险未通过审核", content: "", type: "漏洞消息",…},…]
    0: {id: "2457501", title: "您所提交的漏洞XX登录地址存在可撞库的风险未通过审核", content: "", type: "漏洞消息",…}
    content: ""
    create_time: "2021-07-29 17:06:04"
    id: "2457501"
    otype: "11"
    status: "0"
    title: "您所提交的漏洞XX登录地址存在可撞库的风险未通过审核"
    type: "漏洞消息"
info: "success"
status: 1
'''

# 比对的时间点，从配置文件中读取
if msgJson.get("status") == 1:
    curToken = msgJson.get("data").get("token")
    msgList = msgJson.get("data").get("list")
    maxMsgId = lastMsgId
    for msg in msgList:
        createTime = msg.get("create_time")
        title = msg.get("title")
        id = int(msg.get('id'))
        if id > maxMsgId:
            maxMsgId = id
        if id > lastMsgId:
            print(id, title)
            send_wechat(global_config, 'bt新消息：' + title)
            # 通过计划任务执行时将阻断程序，并且弹窗无法展现给cnzzr
            # os.system('mshta vbscript:msgbox("' + title + '",64,"bt新消息提醒")(window.close)')
            os.system('msg cnzzr /server:127.0.0.1 "id=' + str(id) + ',' + title + '"')

    # 获取排名
    oldRank = global_config.getint("butian", "rank")
    rank = queryRank(global_config, curToken, True)

    # 写配置文件
    if maxMsgId > lastMsgId or (rank is not None and oldRank != rank):
        # 更新指定section，option的值
        global_config.set("butian", "lastMsgId", str(maxMsgId))
        if rank:
            global_config.set("butian", "rank", str(rank))

        # 写回配置文件
        global_config.write(open(ConfigFileName, "w"))

else:
    send_wechat(global_config, 'bt新消息：' + "登录已失效，请更新配置文件cookie值")

print('END')
