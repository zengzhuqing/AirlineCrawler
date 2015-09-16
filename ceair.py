#!/usr/bin/python
#-*- encoding=utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

browser = webdriver.Firefox()
base_url = "http://www.ceair.com/flight2014/"

#store result in ch.out
out_file = "ceair.out"

def get_type_prices(type_name, idx):
	eles = browser.find_elements_by_name(type_name)
	ans = ""
	for e in eles:
		text = e.text
		if text == "":
			continue
		if ord(text[0]) != 65509:
			continue
		for ii in text.split('\n')[0][1:]:
			if ii != ',':
				ans += ii
		ans += "/"
	
	return ans	

def get_prices(ori_code, dest_code, date):
	url = base_url + ori_code + "-" + dest_code + "-" + date + "_CNY.html"
	browser.get(url)

	ret = ["","","",""]

	ret[0] = get_type_prices("first", 0)	
	ret[1] = get_type_prices("business", 1)	
	ret[2] = get_type_prices("economy", 2)	
	ret[3] = get_type_prices("more", 3)	

	return ret

#无dongguan

#上海，哈尔滨，天津，太原，重庆，长春，沈阳，西安，广州，成都，长沙，石家庄，兰州，贵阳，桂林
#三亚，青岛，厦门，深圳，大连，张家界，长白山，泉州，满洲里，武汉，杭州，银川，北京，郑州，南京
#南昌，昆明，济南，福州，合肥，呼和浩特，乌鲁木齐，拉萨，海口，西宁，苏州，无锡，佛山，宁波
#唐山，烟台，南通
cities_code = ['pvg','hrb', 'tsn','tyn','ckg','cgq','she','xiy','can','ctu','csx','sjw','lhw','kwe','kwl','syx','tao','xmn','szx','dlc','dyg','nbs','jjn','nzh','wuh','hgh','inc','nay','cgo','nkg','khn','kmg','tna','foc','hfe','het','urc','lxa','hak','xnn','szv','wux','fuo','ngb', 'tvs','ynt','ntg']
#cities_code = ['SHA','HRB','TSN','NTG']
ori_code = cities_code[0]
dates = []
for i in range(20, 32):
	d = "1510%02d" %(i)
	dates.append(d)
for i in range(1, 31):
	d = "1511%02d" %(i)
	dates.append(d)
for i in range(1, 21):
	d = "1512%02d" %(i)
	dates.append(d)

with open(out_file, 'w+') as f:
	for dest in cities_code[1:]:
		for date in dates:
			#TODO: sleep sometime 
			for ele in get_prices(ori_code, dest, date):
				f.write(ele)
				f.write(" ")
		f.write('\n')

"""
ori_code = "pvg"
dest_code = "kmg"
date="151020"
print get_prices(ori_code, dest_code, date)
"""
browser.quit()
