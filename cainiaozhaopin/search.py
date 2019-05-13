# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from TextM import final,views



import MySQLdb
from TextM.models import jobinfo
def search_form(request):
    return render_to_response('search_form.html')


def search(request):  
    request.encoding='utf-8'
    getinfo(request.GET['q'])
    getinfo2(request.GET['p'])
    getinfo3(request.GET['m'])
    getinfo4(request.GET['form'])
    out = final.main()
    out=  jobinfo.objects.all()
    # views.testdb()
    if request.GET['form']=='form':
        # return render_to_response('test.html')
        return render(request, 'show_jobinfo.html', {'out': out})
    elif request.GET['form']=='Histogram':
        return render_to_response('pictures.html')
    else:
        return render_to_response('wecloud.html')    

def getinfo4(keyword):
    f=open('TextM/info4.txt','w',encoding='utf-8')
    f.write(keyword)
    f.close
    
def getinfo(keyword):
	f=open('TextM/info.txt','w',encoding='utf-8')
	f.write(keyword)
	f.close
	# return txt
def getinfo2(keyword):
    f=open('TextM/info2.txt','w',encoding='utf-8')
    f.write(keyword)
    f.close
    # return 
def getinfo3(keyword):
    f=open('TextM/info3.txt','w',encoding='utf-8')
    f.write(keyword)
    f.close