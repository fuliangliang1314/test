# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from . import main
from flask import render_template, request, jsonify, session, make_response, redirect, url_for
from .response_code import RET
from .my_sql import *
import re
from .mySpider import *
import os
# 主页
@main.route('/')
def login1():
    return render_template('index1.html')
# 登录
@main.route('/login',methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        tel = request.form['tel']
        password = request.form['password']

        data = {
	    "code": 404,
	    "msg": "成功",
	    "result": "-1",
        }


        # 登陆
        #首先校验参数是否完整，包括手机号和密码
        if not all([tel, password]):
            print "登陆参数不完整"
	    return jsonify(errno=RET.PARAMERR, errmsg="登陆参数不完整")
       
        #进一步校验具体的每个参数，手机号格式
        if not re.match(r"^1[34578]\d{9}$", tel):
            print "手机号格式错误"
	    return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")
        #查询数据库操作，对手机号进行进一步验证
        user_login = check_mysql('mobile_user', 'id,password', where='tel="%s"' % tel)
        if not len(user_login):
            print "账号不存在"
	    return jsonify(errno=RET.PARAMERR, errmsg="账号不存在")

        check_password = user_login[0][1]
        if check_password != password:
            print "密码错误"
	    return jsonify(errno=RET.PARAMERR, errmsg="密码错误")

        data['code'] = 200
        data['result'] = '1'
        # 登陆成功，跳转到登陆成功页面
        os.chdir('C:\Users\tuton\Desktop\mobile_API\app\main')  # 必须切换目录，不然爬虫跑不起来
        os.system('python mySpider.py {} &'.format(user_login, check_password))  # 执行命令，让爬虫启动
        print "登陆成功!"
        return jsonify(errno=RET.OK, errmsg="登录成功")



    

