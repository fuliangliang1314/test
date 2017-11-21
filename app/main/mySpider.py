#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from lxml import etree
import time
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
from PIL import Image
import threading
from .login import login
def mobileSpider(dataTime):
    time.sleep(3)
    data = {'PACKAGECODE': 'XD', 'xdFlag': 'GSM', 'month': '%s'%(dataTime)}
    url = 'https://service.bj.10086.cn/poffice/package/xdcx/xdcxShow.action'
    response = requests.post(url, headers=headers, data=data, verify=False)
    html = response.content
    html = etree.HTML(html)
    # 记录通话信息
    call_list = []
    # 记录缴费信息
    pay_list = []
    call_node = html.xpath("//tbody[@id='DETAIL']/tr")
    for node in call_node:
        item = {}
        item["startTime"] = node.xpath("./td[1]/text()")
        item["callCity"] = node.xpath("./td[2]/text()")
        item["callStyle"] = node.xpath("./td[3]/text()")
        item["phoneNumber"] = node.xpath("./td[5]/text()")
        item["callTime"] = node.xpath("./td[6]/text()")
        item["callType"] = node.xpath("./td[7]/text()")
        item["serviceName"] = node.xpath("./td[8]/text()")
        item["callPrice"] = node.xpath("./td[10]/text()")
        for i in range(len(item["phoneNumber"])):
            # 去掉号码里的空格和换行符
            item["phoneNumber"][i] = item["phoneNumber"][i].replace("\t", "").strip()
        call_list.append(item)
    formdata = {'PACKAGECODE': 'XD', 'xdFlag': 'MZLOG', 'month': '%s'%(dataTime)}
    url = 'https://service.bj.10086.cn/poffice/package/xdcx/xdcxShow.action'
    response = requests.post(url, headers=headers, data=formdata, verify=False)
    html = response.content
    html = etree.HTML(html)
    pay_node = html.xpath("//tbody[@id='DETAIL']/tr")
    for node in pay_node:
        item = {}
        # 充值时间
        item["payTime"] = node.xpath("./td[1]/text()")
        # 充值类型
        item["payType"] = node.xpath("./td[2]/text()")
        # 充值金额
        item["payAmount"] = node.xpath("./td[3]/text()")
        # 充值信息存入列表
        pay_list.append(item)
    content = json.dumps(call_list, ensure_ascii=False)
    with open("%scallTest.json"%(dataTime), "w") as f:
        f.write(content)
    payInfo = json.dumps(pay_list, ensure_ascii=False)
    with open("%spayInfo.json"%(dataTime), "w") as f:
        f.write(payInfo)
    time.sleep(1)
if __name__ == "__main__":
    # headless chrome 无界面浏览模式
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/local/bin/chromedriver')
    # 隐式等待最大30s
    driver.implicitly_wait(30)
    driver.get("http://service.bj.10086.cn/poffice/package/xdcx/xdcxShow.action?PACKAGECODE=XD")
    driver.get( "https://bj.ac.10086.cn/ac/cmsso/iloginnew.jsp")
    driver.find_element_by_name("loginName").send_keys(user_login)
    driver.find_element_by_name("password").send_keys(check_password)
    driver.find_element_by_name("rnum").click()
    # 页面截屏，截取验证码区域
    driver.get_screenshot_as_file("Captcha.png")
    im = Image.open("Captcha.png")
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    '''
    x = 310
    y = 145
    w = 128
    h = 50
    region = im.crop((x, y, x+w, y+h))
    region.save("Captcha.png")
    capacha = raw_input("请输入验证码:")
    driver.find_element_by_name("rnum").send_keys(capacha)
    driver.find_element_by_class_name("submit").click()
    # 查询信息需要再次输入服务密码
    driver.find_element_by_xpath('//*[@id="password"]').click()
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("688033")
    driver.find_element_by_xpath(
        '//*[@id="mb-right"]/div/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[6]/td[3]/img').click()
    # 提取cookie
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    # print cookie
    cookiestr = ';'.join(item for item in cookie)
    print cookiestr
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '38',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'service.bj.10086.cn',
        'Origin': 'https://service.bj.10086.cn',
        'Referer': 'https://service.bj.10086.cn/poffice/package/xdcx/xdcxShow.action?PACKAGECODE=XD',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'cookie': cookiestr
    }
    startTime = time.time()
    # 开启多线程爬取1~11月份数据------------------------------------------------------
    #当所有的线程都分配完成之后，通过调用每个线程的start()方法开始执行
    # 相比于管理一组锁（分配、获取、释放、检查锁状态）而言只需要每个线程调用join()的方法
    # 用join()方法等待线程的结束
    threads = []
    t1 = threading.Thread(target=mobileSpider, args=(str(201701),))
    threads.append(t1)
    t2 = threading.Thread(target=mobileSpider, args=(str(201702),))
    threads.append(t2)
    t3 = threading.Thread(target=mobileSpider, args=(str(201703),))
    threads.append(t3)
    t4 = threading.Thread(target=mobileSpider, args=(str(201704),))
    threads.append(t4)
    t5 = threading.Thread(target=mobileSpider, args=(str(201705),))
    threads.append(t5)
    t6 = threading.Thread(target=mobileSpider, args=(str(201706),))
    threads.append(t6)
    t7 = threading.Thread(target=mobileSpider, args=(str(201707),))
    threads.append(t7)
    t8 = threading.Thread(target=mobileSpider, args=(str(201708),))
    threads.append(t8)
    t9 = threading.Thread(target=mobileSpider, args=(str(201709),))
    threads.append(t9)
    t10 = threading.Thread(target=mobileSpider, args=(str(201710),))
    threads.append(t10)
    t11 = threading.Thread(target=mobileSpider, args=(str(201711),))
    threads.append(t11)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    # 统计函数执行时间,保留两位小数
    endTime = time.time()
    print "程序执行时间:%s" % str(round((endTime - startTime), 2)) + "秒"
    # 退出登陆
    driver.find_element_by_xpath('//*[@id="logout"]').click()
    # 关闭浏览器
    driver.quit()

