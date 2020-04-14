from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from api.models import User

# session 只是一个记录功能(会话)　与是否登录没有直接关联
def set_session(request):
    if not request.session.get('num'):
        request.session['num'] = 1
    request.session['num'] += request.session['num']
    nums = request.session['num']
    return HttpResponse(str(nums))

def clean_session(request):
    request.session.clear()
    return HttpResponse('')
