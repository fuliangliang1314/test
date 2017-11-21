from flask import Blueprint
import pymysql
main = Blueprint('main', __name__)

conn =pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='bj',charset="utf8")
cur=conn.cursor()


from . import login
