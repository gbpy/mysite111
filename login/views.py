from django.shortcuts import render,redirect
from . import models
from .forms import UserForm,RegisterForm
import hashlib

# Create your views here.

#主页
def index(request):
    pass
    return render(request,'login/index.html')

#登录
def login(request):
    if request.session.get('is_login',None):  #不允许重复
        return redirect('/index/')
    if request.method =='POST':
        login_form = UserForm(request.POST)
        message = '请检查填写的内容!'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] =user.name
                    return redirect('/index/')
                else:
                    message = '密码不正确!'
            except:
                message = '用户名不存在!'
        return render(request,'login/login.html',locals())
    login_form = UserForm()
    return render(request,'login/login.html',locals())

#注册
def register(request):
    if request.session.get('is_login', None):# 登录状态不允许注册。
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否一致
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新输入！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                #创建新用户
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

#登出
def logout(request):
    if not request.session.get('is_login',None):
        #如果本来就未登录,就没有登出一说
        return redirect('/index/')
    request.session.flush()   #用户退出,删除会话
    return redirect('/index/')

#密码加密
def hash_code(s, salt='mysite111'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # 转换bytes类型
    return h.hexdigest()
















