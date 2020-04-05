from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User


def index(request):
    if request.session.get('is_login'):
        name = request.session['name']
        info = request.session['info']
        data = {'user': {'name': name, 'info': info}}
        return render(request, template_name='login/index.html', context=data)
    return render(request, template_name='login/login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        info = request.POST.get('info')
        try:
            user = User.objects.create(name=name, password=password, info=info)
        except Exception as e:
            return JsonResponse({'msg': e}, status=400)
        return JsonResponse({'user': user.to_json()}, status=200)
    return render(request, template_name='login/register.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = User.objects.filter(name=name, password=password).first()
        if not user:
            return JsonResponse({'msg': '用户不存在!'}, status=400)
        request.session['is_login'] = True
        request.session['name'] = name
        request.session['info'] = user.info
        return JsonResponse({'msg': user.to_json()}, status=200)
    return render(request, template_name='login/login.html')


def logout(request):
    if request.session['is_login']:
        request.session.clear()
    return JsonResponse({'msg': 'register is sucess !'}, status=200)

