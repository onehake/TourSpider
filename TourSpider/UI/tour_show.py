#!/usr/bin/python
# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置
import json
import tkinter as tk
from tkinter import ttk


root=tk.Tk()
root.title("评论信息总览")
root.geometry('800x300')        #设置窗口大小
root.resizable(width=False, height=True)    #宽不变，高可变，默认为Ture

frame = tk.Frame(root)
frame.pack()
country = tk.StringVar()
jd = tk.StringVar()
time = tk.StringVar()

country_L = tk.Label(frame,text="国家").pack(side="left")
country_E = tk.Entry(frame, textvariable = country).pack(side="left")
jd_L = tk.Label(frame,text="景点").pack(side="left")
jd_E = tk.Entry(frame, textvariable = jd).pack(side="left")
time_L = tk.Label(frame,text="时间").pack(side="left")
time_E = tk.Entry(frame, textvariable = time).pack(side="left")


def find():
    settings = get_project_settings()  # 获取settings配置，设置需要的信息
    dbparams = dict(
        host=settings['MYSQL_HOST'],  # 读取settings中的配置
        db=settings['MYSQL_DBNAME'],
        user=settings['MYSQL_USER'],
        passwd=settings['MYSQL_PASSWD'],
        charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
        cursorclass=pymysql.cursors.DictCursor,
        use_unicode=False,
    )
    conn = pymysql.connect(**dbparams)
    cursor = conn.cursor()
    # encoding=utf8

    country1 = country.get()
    jd1 = jd.get()
    time1 = time.get()
    # 执行SQL，并返回收影响行数
    sql = "select *  from tourdata where 1=1"  # 去重插入
    # 调用插入的方法
    #"select * from '" + table + "'"
    if country1 != "":
        sql += " and country = '" + country1 + "'"
    if jd1 != "":
        sql += " and jd like  '%" + jd1 + "%'"
    if time1 != "":
        sql += " and time like '%"+ time1 + "%'"
    sql += ' limit 500'
    print(sql)
    cursor.execute(sql)
    rs = cursor.fetchall()

    x = tree.get_children()
    for item in x:
        tree.delete(item)

    for r in rs:
        #r.encode('utf-8')
        tree.insert("", 1, values=(r['country'].decode(), r['jd'].decode() , r['comm'].decode() , r['name'].decode() , r['time'].decode()))





    conn.commit()
    cursor.close()
    conn.close()

    pass

query = tk.Button(frame,text="查询" , command=find).pack(side="left")

table_frame = tk.Frame(root)

tree = tk.ttk.Treeview(table_frame)  # 表格
tree["columns"] = ("国家", "景点", "评论","用户","时间")
tree.column("国家", width=100 , anchor='center')  # 表示列,不显示
tree.column("景点", width=100 , anchor='center')
tree.column("评论", width=100 , anchor='center')
tree.column("用户", width=100 , anchor='center')
tree.column("时间", width=100 , anchor='center')

tree.heading("国家", text="国家")  # 显示表头
tree.heading("景点", text="景点")
tree.heading("评论", text="评论")
tree.heading("用户", text="用户")
tree.heading("时间", text="时间")

tree.pack()

table_frame.pack()

root.mainloop()
