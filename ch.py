#!/usr/bin/python
#-*- encoding=utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

browser = webdriver.Firefox()
base_url = "http://flights.ch.com/"
class_name = 'f-ib'

#store result in ch.out
out_file = "ch-" + time.strftime("%Y-%m-%d", time.localtime(time.time())) + ".out"

def get_prices(ori_code, dest_code, date):
	url = base_url + ori_code + "-" + dest_code + ".html?SType=0&IfRet=false&Oricode=" + ori_code + "&DestCode=" + dest_code + "&MType=0&FDate=" + date + "&ANum=1&CNum=0&INum=0"
	browser.get(url)
	eles = browser.find_elements_by_class_name(class_name)
	
	ans = []
	for e in eles:
		text = e.text
		if text == "":
			continue
		if ord(text[0]) == 45:
			ans.append('--')
		elif ord(text[0]) == 0xa5:
			ans.append(text.split('\n')[0][2:])
	
	ret = ["","",""]
	for i in range(0, len(ans)):
		if i % 6 == 0:
			ret[0] += ans[i]
			ret[0] += "/"
		elif i % 6 == 1:
			ret[1] += ans[i]
			ret[1] += "/"
		elif i % 6 == 2:
			ret[2] += ans[i]	
			ret[2] += "/"
	
	return ret

#无济南,拉萨,xining,foshan,dongguan

#上海，哈尔滨，天津，太原，重庆，长春，沈阳，西安，广州，成都，长沙，石家庄，兰州，贵阳，桂林
#三亚，青岛，厦门，深圳，大连，张家界，长白山，泉州，武汉，杭州，北京，郑州，海口，昆明，乌鲁木齐
#满洲里，银川，南京，南昌，福州，合肥，呼和浩特，苏州，无锡，宁波，唐山
#烟台，南通
cities_code = ['SHA','HRB', 'TSN','TYN','CKG','CGQ','SHE','SIA','CAN','CTU','CSX','SJW','LHW','KWE','KWL','SYX','TAO','XMN','SZX','DLC','DYG','BAS','JJN','WUH','HGH','PEK','CGO','HAK','KMG','URC','NZH','INC','NKG','KHN','FOC','HFE','HET','SZV','WUX','NGB','TVS','YNT','NTG']
#cities_code = ['SHA','HRB','TSN','NTG']
ori_code = cities_code[0]
dates = []
for i in range(20, 32):
	d = "2015-10-%02d" %(i)
	dates.append(d)
for i in range(1, 31):
	d = "2015-11-%02d" %(i)
	dates.append(d)
for i in range(1, 21):
	d = "2015-12-%02d" %(i)
	dates.append(d)

with open(out_file, 'w+') as f:
	for dest in cities_code[1:]:
		for date in dates:
			for ele in get_prices(ori_code, dest, date):
				f.write(ele)
				f.write(" ")
		f.write('\n')

#print get_prices(ori_code, dest_code, date)

browser.quit()
