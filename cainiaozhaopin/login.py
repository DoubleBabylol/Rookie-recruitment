from django.shortcuts import render
# Create your views here.
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.shortcuts import redirect  #重新定向模块

def login_form(request):
    return render(request,'login.html')

def login(request):
     #包含用户提交的所有信息
     #获取用户提交方法
    #print(request.method)
    error_msg = ""
        #获取用户通过POST提交过来的数据
    user =request.POST.get('user',None)
    pwd =request.POST.get('pwd',None)
            #去跳转到
        #f=open('info4.txt','w',encoding='utf-8')
       # f.write(user)
    user = authenticate(request, username=user, password=pwd)
    if user is not None:
        return  render(request,'search_form.html')            #用户密码不匹配
           # error_msg = '用户名或密码错误'
        # user = request.POST['user']
        # pwd = request.POST['pwd']
        # print(user,pwd)
    else:
        return render(request,'login.html',{'error_msg':error_msg})


