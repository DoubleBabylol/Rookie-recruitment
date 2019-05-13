#coding:utf8
import sys
from pandas import DataFrame  #DataFrame通常来装二维的表格
import pandas as pd
from sqlalchemy import create_engine
#清空之前的查询数据库
import MySQLdb
# 打开数据库连接
db=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='django')
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
# SQL 删除语句
sql = "DELETE FROM django_double "
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交修改
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()

# 关闭连接
db.close()


#查询结果重新入库
data = pd.read_table('51job.txt',names=['one','two','three','four','five'],encoding='utf-8')
print(data)
engine=create_engine("mysql+pymysql://root:123456@localhost:3306/django?charset=utf8",echo=True)
pd.io.sql.to_sql(data,'django_double', engine, schema='django', if_exists='append')
