# coding=utf-8
from . import cur, conn
import pymysql
from flask import render_template, request, jsonify, session, make_response, redirect, url_for, g
import functools
import calendar

# 查询
def check_mysql(tables=None, column='*', where=None, sql=None):
    if sql:
        employee = cur.execute(sql)
        return cur.fetchall()

    if where:
        sql = 'select %s from %s where %s' % (column, tables, where)
        # print(sql)
        employee = cur.execute(sql)
        return cur.fetchall()


    sql = 'select %s from %s' % (column, tables)
    employee = cur.execute(sql)
    return cur.fetchall()




# 保存
def save_mysql(tables, data):
    '''
    例：
    data['user_id'] = user_id
    data['value'] = value
    data['time'] = time.time()
    save_mysql('session', data)
    :param tables:表名
    :param data: 字典　键：字段　值：值　
    :return:
    '''
    fields = ''
    values = ''
    for k, v in data.items():
        fields += str(k) + ','
        values += '"%s",' % str(v)

    sql = 'insert into %s(%s) values(%s);' % (tables, fields[:-1], values[:-1])
    print(sql)
    employee = cur.execute(sql)
    conn.commit()
    return employee

# 修改
def update_mysql(tables, data, where):
    '''
    例子：update_mysql('admin_role', {'exempla':'角色'}, 'role="角色D"')
    '''
    set = ''
    for k, v in data.items():
        if type(1) == type(v):
            set += '%s=%d,' % (k, v)
            continue
        set += '%s="%s",' % (k, v)
    sql = 'update %s set %s where %s' % (tables, set[:-1], where)
    print(sql)
    employee = cur.execute(sql)
    conn.commit()
    return employee
