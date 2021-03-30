# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
import datetime
import ssl
import json
import datetime
#from HandleCsv import HandleCsv
#from Send_Wechart import Send_Wechart
#from Send_Email import Send_Email
import csv
import time
import datetime

requests.packages.urllib3.disable_warnings()
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

url_price = "https://www.microsoftstore.com.cn/certified-refurbished-surface-go-configurate"
#url_price = "https://www.microsoftstore.com.cn"
def getYesterday(): 
    today=datetime.date.today() 
    print("今天的时间:",today)
    #str = '2012-11-01'
    #today = datetime.datetime.strptime(str,'%Y-%m-%d')
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    yesterday = yesterday.strftime("%Y-%m-%d")
    yesterday = yesterday.replace('-','年',1)
    yesterday = yesterday.replace('-','月',1)
    yesterday += '日'
    yesterday.replace(' ','')
    print("昨天时间为1：",yesterday) 
    
    return yesterday

def replace_char(string,char,index):
     string = list(string)
     string[index] = char
     return ''.join(string)

def url_open(url_all):
    try:
        page_headers={
             'Accept': 'application/json, text/javascript, */*; q=0.01',
             'Host': 'www.microsoftstore.com.cn',
             'Referer': 'https://www.microsoftstore.com.cn',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

        try:
            res=requests.post(url_price,headers=page_headers)
        except:
            print("出错")
          
        html = res.text

        file_handle = open('C:\\Users\\Jamly\\Desktop\\test.txt','w',encoding='utf-8')
        file_handle.write(html)
        file_handle.close()

        status=res.status_code
        if status!= 200:
            print("访问异常")
            return '-1'
        else:
            #print("status:",status)
            data=res.text
            return data
    except:
        pass

def get_string(data):
    c = "["
    try:
        res = None
        for i in range(0, len(data)): 
            if ini_string[i] == c: 
                res = i + 1
                break
            
        if res == None: 
            print ("No such charater available in string") 
        else: 
            print ("Character {} is present at {}".format(c, str(res))) 

    except:
        return "找不到数据"

def porcess_wechart():
    wechart_send = Send_Wechart(u'jamly_liu')
    wechart_send.send_move(u'jamly_liu','jamly_liu')

def porcess_csv(dict_txt,time,list_dic):
    #list_date = list_dic[0]
    list_data = list_dic[1]

    dict_txt[time] = list_data[int(list_dic[2])-1]#list_dic[2]为list的漂移量，dict_txt为字典数据
    h_csv = HandleCsv(u'C:/Users/liuzj/Desktop/gold/data_test.csv')
    csv_line = h_csv.get_list_len(0)#拿到行数
    print("csv行数为:",csv_line)
    #print("day_date[11:16]:",day_date[11:16])
    #print("day_tmp数据为：",day_tmp)
    h_csv.insert_row(csv_line+1)
    h_csv.insert_col(csv_line+1, 1, time[0:10])#日期
    h_csv.insert_col(csv_line+1, 2, time[11:16])#时间
    h_csv.insert_col(csv_line+1, 3, dict_txt[time])#数值
    h_csv.list2csv(u'C:/Users/liuzj/Desktop/gold/data_test.csv')
    return dict_txt


def change_csv(list_dic):
    #list_date = list_dic[0]
    #list_data = list_dic[1]
    len1 = len(list_dic[0])
    print("len长度:",len1)
    h_csv = HandleCsv(u'C:/Users/liuzj/Desktop/gold/data_get1.csv')
    #for i in list_dic[0] :
    for i in range(0,782):
        csv_line = h_csv.get_list_len(0)#拿到行数
        print("csv行数为:",csv_line)
        h_csv.insert_row(csv_line+1)
        h_csv.insert_col(csv_line+1, 1, list_dic[0][i])#时间
        h_csv.insert_col(csv_line+1, 2, list_dic[1][i])#数值
        #h_csv.insert_col(csv_line+1, 2, i)
        #print("list_date:",list_date,"list_data:",list_data)
        h_csv.list2csv(u'C:/Users/liuzj/Desktop/gold/data_get1.csv')




def porcess_dict(list_dic):
    list_date = list_dic[0]
    #list_data = list_dic[1]

    file = open('C:\\Users\\liuzj\\Desktop\\gold\\dict.txt','r') 
    f1 = file.read()
    file.close()  
    print("dict.txt数据为：",f1) 
    dict_txt = eval(f1)
    print("dict.txt为：",dict_txt) 
    if list_date[0] in f1:
        print("存在")
        return '1'
    else:
        #如果当前时间为00:00，那取-1的时间就是跨天了，要对记录的时间做处理
        list_tmp = list_dic[3]
        list_tmp = list_tmp[12:17]
        if list_tmp == '00:00':
            print("数据跨天了：",list_tmp) 
            day_date = getYesterday()
        else:
            list_tmp = list_dic[3]
            day_date = list_tmp[0:11]    
        
        day_date += list_date[int(list_dic[2])-1]#加上时间

    str_txt = str(porcess_csv(dict_txt,day_date,list_dic))
    change_csv(list_dic)
    #print("最后数据：",str_txt)
    file = open('dict.txt', 'w') 
    file.write(str_txt)
    file.close()  
    return '0'

#def process_monitor(subject,now_price): #判断当前价格与24小时前差值，通过position比较

#与昨天的第239个数据比较(59分)
def check_price(list_dic):
    return 1

def check_time():#检测当前时间是否可比较    
    #str = '2021-02-28'
    #today1 = datetime.datetime.strptime(str,'%Y-%m-%d')
    week = datetime.date.today().strftime('%w')#星期天:0,0-6
    print("今天星期几：",week)
    h=datetime.datetime.now()
    time_now=h.strftime("%H:%M:%S")  
    print("今天时间：",time_now)
    #time_now = datetime.datetime.now().strftime("%H:%M:%S")
    #week = today.strftime('%w')
    if week == 5 or week == 0:  #周六和周日不检测
        return -1
    else:
        return 0
        
if __name__ == '__main__':
    data = url_open(url_price)
    #subject = get_data()
    #porcess_dict(subject)
    #today_data=get_today()
    #get_time()
    #check_time()
    #email_send = Send_Email(u'jamly_liu')
    #email_send.send_mail()
    #porcess_wechart()  #微信处理
    #content="今天是"+today_data+","+subject
    #print(content)
    # mail_qq(subject,content)
    
#测试