# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response

def picture(request):
    return render_to_response('pictures.html')