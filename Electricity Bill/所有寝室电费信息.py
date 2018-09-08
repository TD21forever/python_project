import requests
import json
from bs4 import BeautifulSoup
import time
import re
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient("localhost",27017)
title =client["title"]
sheet_table_one = title['sheet_table_one']
sheet_table_two = title['sheet_table_two']

def get_build_id():
    url = "http://wap.xt.beescrm.com/base/common/getBuildingList"

    headers ={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
    }
    form_data = {
        'id': '57'
    }

    wb_data = requests.post(url,headers = headers,data = form_data)
    json_data = json.loads(wb_data.text)
    for one in json_data["data"]:
        yield  one['building_id']




def get_floor_id(floor_id):
    url = "http://wap.xt.beescrm.com/base/common/getFloorList"

    headers ={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
    }
    form_data2 = {
        'id': floor_id
    }

    wb_data = requests.post(url,headers = headers,data = form_data2)
    json_data2 = json.loads(wb_data.text)

    for one in json_data2["data"]:
        yield one["floor_id"]


def get_room_id(room_id):
    url = "http://wap.xt.beescrm.com/base/common/getRoomList"



    headers ={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
    }
    form_data3 = {
        'id': room_id
    }

    wb_data = requests.post(url,headers = headers,data = form_data3)
    json_data3 = json.loads(wb_data.text)
    for one in json_data3["data"]:
        yield one["room_id"]

# if __name__ == '__main__':
#     for one in get_build_id():
#         for two in get_floor_id(one):
#             for three in get_room_id(two):
#                 data = {
#                     "url": "http://wap.xt.beescrm.com/base/electricityHd/queryResult/ele_id/7/community_id/57/building_id/{}/floor_id/{}/room_id/{}/flag/1".format(
#                         one, two, three)
#                 }
#                 sheet_table_one.insert_one(data)

class EleM(object):

    def get_info(self,url):

        headers={
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        try:

            wb_data = requests.get(url,headers= headers)
            soup =  BeautifulSoup(wb_data.text,"lxml")
            info = soup.select('div.info-box p')
            time = soup.select("font b")
            data = {
                "time":time[0].text,
                "money":info[0].text,
                "place":info[1].text,
                "building":info[2].text,
                "floor":info[3].text,
                "room":info[4].text
            }
            print(data)
            sheet_table_two.insert_one(data)
        except:
            pass
        # for one in info:
        #     info_text = one.text
        #     try:
        #         match = re.search(r"\d+\.*\d*",info_text)
        #         str+=match.group()+"a"
        #     except:
        #         pass
        #
        # print(str)


if __name__ == '__main__':
    money = EleM()
    item_url_list =[item["url"] for item in sheet_table_one.find()]
    pool = Pool()
    pool.map(money.get_info,item_url_list)





