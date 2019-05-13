import urllib.request
import re
import requests
import numpy
import os
import lxml
import matplotlib.pyplot as plt
import jieba
from nltk import *
from wordcloud import WordCloud

import sys
from pandas import DataFrame  #DataFrame通常来装二维的表格
import pandas as pd
from sqlalchemy import create_engine
#清空之前的查询数据库
import MySQLdb
from TextM.models import jobinfo

#获取原码
def get_content(keyword,page):
    url ='http://search.51job.com/list/000000,000000,0000,00,9,99,'+ keyword + ',2,'+ str(page)+'.html'
    a = urllib.request.urlopen(url)#打开网址
    html = a.read().decode('gbk')#读取源代码并转为unicode
    return html

def get(html):
    reg = re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)".*? <span class="t2"><a target="_blank" title="(.*?)" href="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*? <span class="t5">(.*?)</span>',re.S)#匹配换行符
    items=re.findall(reg,html)
    return items
#多页处理，下载到文件

def gongzi(s):
    if len(s)==0:
        return -1
    result = 0.0
    point = False
    cnt = 1
    num = '0123456789'
    for ch in s:
        if ch != '.' and ch not in num:
            break
        if ch =='.':
            point=True
            continue
        if point == False:
            result = result * 10 + int(ch)
        else:
            result = result + int(ch) * pow( 10 , -cnt)
            cnt = cnt + 1
    if '万' in s:
        result =result *10000
    elif '千' in s :
        result = result * 1000
    elif '元' in s:
        result = result
    else:
        return -1
    if '月' in s:
        return result
    elif '年' in s:
        return result // 12
    elif '天' in s:
        return result * 20
    else :
        return -1


def get_pagenum(html):
    reg = re.compile(r'div class="dw_page">.*?</a></li></ul><span class="td">(.*?)</span><input id="jump_page" class="mytxt" type="text" value=', re.S)
    items = re.findall(reg, html)
    return items

def main():
    
    with open('TextM/51job.txt', "r+", encoding='utf-8') as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()   #清空文件
    f.close()
    with open('TextM/data.txt', "r+", encoding='utf-8') as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()   #清空文件
    f.close()
    f = open('TextM/info.txt' ,'r', encoding='utf-8')
    keyword=f.read()#职业
    f.close()
    f = open('TextM/info2.txt','r', encoding='utf-8')
    area = f.read()#地区
    f.close()
    f =open('TextM/info3.txt','r', encoding='utf-8')
    money = int(f.read())#工资
    f.close()
    #print(keyword)
    #print(area)
    #print(money)


    companylist=[]
    salarylist=[]
    cnt = 0 
    totalpage = 0
    num = 50
    html = get_content(keyword, 1)
    temp = get_pagenum(html)
    #print(temp)
    for c in temp:
        for ch in c:
            if ch >= '0' and ch <= '9':
                totalpage = totalpage * 10 + int(ch)
    print(totalpage)#总页数
    for  j in range(totalpage):
        print("getting the "+str(j)+" page of data...")
        html=get_content(keyword,j)#调用获取网页原码
        #print(get_pagenum(html))
        for i in get(html):
                if area not in i[3]:
                    continue
                if gongzi(i[4]) < money:
                    continue
                #print(i[0]+'\t'+i[1]+'\t'+i[2]+'\t'+i[3]+'\t'+i[4]+'\n')
                companylist.append(i[1])
                salarylist.append(int(gongzi(i[4])))
                with open ('TextM/data.txt','a',encoding='utf-8') as f:
                    f.write(i[0]+'\n')
                    f.close()
                with open ('TextM/51job.txt','a',encoding='utf-8') as f:
                    f.write(i[0]+'\t'+i[1]+'\t'+i[2]+'\t'+i[3]+'\t'+i[4]+'\n')
                    f.close()

                cnt = cnt +1
                if cnt > num:
                    break
        if cnt > num:
            break
            

    words = []
    with open('TextM/data.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            seg_list = jieba.cut(line, cut_all=False)
            for w in seg_list:
                words.append(w)
    f.close()
    wcloud = "static/wcloud.png"
    fdist = FreqDist(words)
    fd_sort = sorted(fdist.items(), key=lambda d: d[1],reverse=True)

    wc1 = WordCloud(
        background_color="white",
        font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",#不加这一句显示口字形乱码
    )
    wc2 = wc1.generate(' '.join(words))
    wc2.to_file(wcloud)
    """
    plt.imshow(wc2)
    plt.axis("off")
    plt.show()
    """
    
    #柱状图生成
    plt.bar(range(len(salarylist)), salarylist,color='rgb',tick_label=companylist)
    plt.savefig("static/barChart.jpg")
    #plt.show()
    #print (salarylist)









#     db=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='django')
# # 使用cursor()方法获取操作游标 
#     cursor = db.cursor()
#     # SQL 删除语句
#     sql = "DELETE FROM textm_jobinfo "
#     try:
#        # 执行SQL语句
#        cursor.execute(sql)
#        # 提交修改
#        db.commit()
#     except:
#        # 发生错误时回滚
#        db.rollback()

#     # 关闭连接
#     db.close()
    out = jobinfo.objects.all()
    out.delete()


    #查询结果重新入库
    data = pd.read_table('TextM/51job.txt',names=['jobname', 'company', 'url', 'location', 'salary'],encoding='utf-8')
    print(data)
#     engine=create_engine("mysql+pymysql://root:123456@localhost:3306/django?charset=utf8",echo=True)
#     pd.io.sql.to_sql(data,'django_double', engine, schema='django', if_exists='append')
    data.apply(lambda s:save(s), axis=1)
    out = jobinfo.objects.all()
    return out


def save(s):
    q = jobinfo(jobname=s['jobname'], company=s['company'], url=s['url'], location=s['location'], salary=s['salary'])
    q.save()



if __name__ == "__main__":
    main()