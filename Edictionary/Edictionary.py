import tkinter as tk
import requests
from tkinter import messagebox
from requests.exceptions import*
import json


def get_post_data(word,which_lan):
	headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
	url = "http://fanyi.baidu.com/langdetect"

	form_data = {
		'query': word
	}
	wb_data = requests.post(url,headers= headers,data= form_data)
	
	json_data = json.loads(wb_data.text)

	data_from = json_data['lan']
	# which_lan = input("1--->中文\n"+"2--->英文\n"+"3--->文言文\n"+"4--->阿拉伯语\n"+"5--->德语\n"+"6--->韩语\n"+"7--->泰语\n"+"8--->法语\n"+"您想翻译成那种语言\n")

	to_dict  = {'1':'zh','2':'en','3':'wyw','4':'ara','5':'de','6':"kor","7":"th",'8':'fra'
}
	post_data  ={
	'query': word,
	'from': data_from,
	'to': to_dict.get(which_lan)
	}

	return post_data


def get_trans_result(data):
	headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
	url = "http://fanyi.baidu.com/basetrans"

	wb_data = requests.post(url,headers = headers,data =data)
	json_data = json.loads(wb_data.text)

	trans_result = json_data['trans'][0]['dst']
	return trans_result
	

def main():
	words = input("请输入您想查询的词或句子\n")
	post_data = get_post_data(words)
	trans_result = get_trans_result(post_data)


window = tk.Tk()
window.title("Edictionary")
window.geometry("400x400")

first_label = tk.Label(window, text = "请输入您想查询的词或句子",font=("正楷",12))
first_label.place(x=0,y=10)
var_entry = tk.StringVar()
var = tk.StringVar()
var_result = tk.StringVar()
entry = tk.Entry(window,textvariable = var_entry)
entry.place(x=0,y=30)

def translate():
	try:
		words = entry.get()
		which_lan = var.get()
		post_data = get_post_data(words,which_lan)
		trans_result = get_trans_result(post_data)
		text_info.delete(0.0,"end")
		text_info.insert("insert",trans_result +'\n')
	except (TypeError,ValueError,KeyError) :
		text_info.delete(0.0,"end")
		text_info.insert("insert","请不要选择同一种语言\n")
	except (RuntimeError,ConnectionError):
		tk.messagebox.showerror(title = " Error", message = "超时请重试")


button = tk.Button(window,text = "翻译",command= translate)
button.place(x=150,y=30)

rb_1 = tk.Radiobutton(window,text = "1--->中文",width = 15, height = 1, variable = var,value = '1')
rb_2 = tk.Radiobutton(window,text = "2--->英文",width = 15, height = 1, variable = var,value = '2')
rb_3 = tk.Radiobutton(window,text = "3--->文言文",width = 15, height = 1, variable = var,value = '3')
rb_4 = tk.Radiobutton(window,text = "4--->阿拉伯语",width = 15, height = 1, variable = var,value = '4')
rb_5 = tk.Radiobutton(window,text = "5--->德语",width = 15, height = 1, variable = var,value = '5')
rb_6 = tk.Radiobutton(window,text = "6--->韩语",width = 15, height = 1, variable = var,value = '6')
rb_7 = tk.Radiobutton(window,text = "7--->泰语",width = 15, height = 1, variable = var,value = '7')
rb_8 = tk.Radiobutton(window,text = "8--->法语",width = 15, height = 1, variable = var,value = '8')

text_info = tk.Text(window,height = 20)
text_info.place(x=150,y=80)

rb_1.place(x=0,y=50)
rb_2.place(x=0,y=90)
rb_3.place(x=0,y=130)
rb_4.place(x=0,y=170)
rb_5.place(x=0,y=210)
rb_6.place(x=0,y=250)
rb_7.place(x=0,y=290)
rb_8.place(x=0,y=320)

window.mainloop()