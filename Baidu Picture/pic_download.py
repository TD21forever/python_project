import tkinter as tk
from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import urlencode
from requests.exceptions import RequestException
import urllib.request
import json
from multiprocessing import Pool
import os

def get_page_html(word="柴犬",pages=1):
	url_list=[]
	for i in range(30,30*pages+30,30):
		data ={
			'tn': 'resultjson_com',
			'ipn': 'rj',
			'ct': '201326592',
			'is':'',
			'fp': 'result',
			'queryWord':word,
			'cl': '2',
			'lm': '-1',
			'ie': 'utf - 8',
			'oe': 'utf - 8',
			'adpicid':'',
			'st': '-1',
			'word': word,
			'z':'',
			'ic': '0',
			's':'',
			'se':'',
			'tab':'',
			'width':'',
			'height':'',
			'face': '0',
			'istype':' 2',
			'qc':'',
			'nc': '1',
			'fr':'',
			'step_word': word,
			'pn': i,
			'rn': '30',
			'gsm':'1',
			'e':'',
			'1520497137736':'',
		}
		url = "http://image.baidu.com/search/index?"+urlencode(data)
		# print(url)
		url_list.append(url)
	return url_list

def get_page_url(word,page):
	url_list = get_page_html(word,page)
	for one in url_list:
		wb_data = requests.get(one,headers=headers)
		if wb_data.status_code == 200:
			html = wb_data.text
			# print(html)
			data = json.loads(html)
		else:
			print("请求失败")
		if data and "data" in data.keys():
			url_list = [one.get("thumbURL") for one in data["data"]]
			# print(url_list)
			yield url_list

def download(url):
	time.sleep(2)
	try:
		urllib.request.urlretrieve(url,"picture/"+url[-20:])
		print("ok")
		info_text.insert("insert","ok\n")

	except:
		print("fail")
		info_text.insert("insert","fail\n")


def main(word,page):
	
	pool = Pool()
	for one in get_page_url(word,page):
		# print(one)
		pool.map(download,one)

def download_button():
	if not os.path.exists("picture/"):
		os.mkdir("picture/")
	keyword = var_keyword.get()
	page = var_page.get()
	for urls in get_page_url(keyword,page):
		for url in urls:
			download(url)


window = tk.Tk()
window.title("Picture download")
window.geometry("400x400")

keyword_label = tk.Label(window,text = "Key words",font=("",12))
keyword_label.place(x=10,y=40)
page_label = tk.Label(window,text = "Page",font=("",12))
page_label.place(x=10,y=90)


var_keyword = tk.StringVar()
var_page= tk.IntVar()

keyword_entry = tk.Entry(window,textvariable = var_keyword)
keyword_entry.place(x=120,y=40)
keyword_entry = tk.Entry(window,textvariable = var_page)
keyword_entry.place(x=120,y=90)

button = tk.Button(window,text = "Dowload",command = download_button)
button.place(x=270,y=60)

info_text = tk.Text(window,height = 10,width = 70)
info_text.place(x=0,y=150)

headers ={
   "Cookie" :"BAIDUID=8DB47D5945E93E2957A2870DC4497156:FG=1; BIDUPSID=8DB47D5945E93E2957A2870DC4497156; PSTM=1535723260; PSINO=7; locale=zh; pgv_pvi=3838617600; pgv_si=s3318363136; H_PS_PSSID=1429_21118_26350_20928; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=www.baidu.com; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; indexPageSugList=%5B%221%22%2C%22welcome.png%22%5D; cleanHistoryStatus=0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm",
   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}


window.mainloop()