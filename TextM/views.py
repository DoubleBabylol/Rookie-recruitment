# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
#from TextM import models
#from TextM import duqutxt
import MySQLdb
import pandas as pd
# Create your views here.
'''def testdb(request):
	#obj=models.DjangoDouble.objects.all()
	#obj=duqutxt.data
	data = pd.read_table('TextM/51job.txt',names=['one','two','three','four','five'],encoding='utf-8')

	return render(request,'test.html',{'o':data})'''
def testdb():
	data = pd.read_table('TextM/51job.txt',names=['职位','名称','地点','薪资','日期'],encoding='utf-8')
	res = data.to_html(index=False)
	with open('templates/test.html', 'w', encoding='utf-8') as f:
		f.write(res)
