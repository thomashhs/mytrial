#coding:utf-8
from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from .forms import RegisterForm,LoginForm,PasswordForm,PasswordResetForm
from .models import User,Logacn,Logtxn,Post,Category,Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown
from .models import Comment
from .forms import CommentForm
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.core.mail import send_mail
import string
import random
import datetime

# Create your views here.
def index(request):
    user_email=request.COOKIES.get('user_email')
    post_list=Post.objects.all()

    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)


    return render(request, 'third/index.html',context={'user_email':user_email,'post_list':post_list})

###用户注册
def signup(request):
    errors=[]
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():
            user_email=form.cleaned_data['email']
            user_password1 = form.cleaned_data['password1']
            user_password2 = form.cleaned_data['password2']

            if(user_password1!=user_password2):
                errors.append('两次密码输入不一致')
                return render(request, 'third/sign_up.html',context={'form':form,'errors':errors})

            if User.objects.filter(email__exact=user_email):
                errors.append('该邮箱已注册')
                return render(request, 'third/sign_up.html',context={'form':form,'errors':errors})

            User.objects.create(email=user_email,password=user_password1)
            errors.append('恭喜，该邮箱已成功注册，请登录')
            return render(request, 'third/sign_up.html',context={'form':form,'errors':errors})
    else:
        form=RegisterForm()
    return render(request, 'third/sign_up.html',context={'form':form})

###用户登录
def signin(request):
    errors=[]
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']

            if not User.objects.filter(email__exact=user_email):
                errors.append('该邮箱不存在，请注册')
                return render(request, 'third/sign_in.html', context={'form': form, 'errors': errors})
            if not User.objects.filter(email__exact=user_email,password__exact=user_password):
                errors.append('邮箱或密码错误，请重新输入')
                return render(request, 'third/sign_in.html', context={'form': form, 'errors': errors})

            response = redirect('third:index')
            response.set_cookie('user_email',user_email,3600)
            return response
    else:
        form=LoginForm()
    return render(request, 'third/sign_in.html',context={'form':form})

def logout(request):
    response = redirect('third:index')
    response.delete_cookie('user_email')
    return response

###修改密码
def password_change(request):
    errors = []
    user_email = request.COOKIES.get('user_email')
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password_origin = form.cleaned_data['password_origin']
            password_new = form.cleaned_data['password_new']
            password_verify = form.cleaned_data['password_verify']

            if not User.objects.filter(email__exact=user_email,password__exact=password_origin):
                errors.append('用户原密码错误，请重新输入')
                return render(request, 'third/password_change.html', context={'form': form, 'user_email':user_email,'errors': errors})

            if (password_new != password_verify):
                errors.append('两次新密码输入不一致')
                return render(request, 'third/password_change.html', context={'form': form, 'user_email':user_email,'errors': errors})

            User.objects.filter(email__exact=user_email, password__exact=password_origin).update(password=password_new)
            errors.append('恭喜，用户密码已成功修改')
            return render(request, 'third/password_change.html', context={'form': form, 'user_email':user_email,'errors': errors})
    else:
        form=PasswordForm()
    return render(request, 'third/password_change.html', context={'form': form,'user_email':user_email})

###密码重置
def password_reset(request):
    errors=[]
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email=form.cleaned_data['email']
            if not User.objects.filter(email__exact=user_email):
                errors.append('注册邮箱不存在，请重新输入')
                return render(request, 'third/password_reset.html', context={'form': form, 'errors': errors})



            date_reset=User.objects.filter(email__exact=user_email).values("date_reset")[0]['date_reset']
            date_now=datetime.datetime.now()


            if not date_reset:
                pass
            elif date_now - date_reset < datetime.timedelta(hours=1):
                errors.append('密码重置时间间隔不足1小时')
                return render(request, 'third/password_reset.html', context={'form': form, 'errors': errors})

            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            User.objects.filter(email__exact=user_email).update(password=salt,date_reset=date_now)

            msg = '<p>您的重置密码是： '+salt+' 请使用新密码登录并修改个人密码。</p>'
            send_mail('标题', '内容', 'TinyShu<django_tinyshu@163.com>',
                      ['345870016@qq.com'],
                      html_message=msg)
            errors.append('用户密码已重置，请登录邮箱获取')
            return render(request, 'third/password_reset.html', context={'form': form, 'errors': errors})
    else:
        form = PasswordResetForm()
    return render(request, 'third/password_reset.html', context={'form': form})

def about(request):
    log_list = Logacn.objects.order_by('-pub_date')
    paginator = Paginator(log_list, 4)
    page = request.GET.get('page')
    user_email = request.COOKIES.get('user_email')

    try:
        log_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        log_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        log_list = paginator.page(paginator.num_pages)

    return render(request,'third/about.html',context={'log_list':log_list,'user_email':user_email})

def tool(request):
    user_email = request.COOKIES.get('user_email')
    return render(request,'third/tool.html',context={'user_email':user_email})

def toolname(request,tool_name):
    user_email = request.COOKIES.get('user_email')
    return render(request,'third/'+tool_name+'.html',context={'user_email':user_email})

##博客详情
def detail(request,post_id):
    user_email = request.COOKIES.get('user_email')
    post=get_object_or_404(Post,pk=post_id)
    md = markdown.Markdown(post.content,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                          TocExtension(slugify=slugify),
                                     ])

    post.content = md.convert(post.content)
    post.toc = md.toc
    #判断是否包含markdown目录
    if post.toc.find('li')==-1:
        post.toc=None
    form = CommentForm()
    comment_list = post.comment_set.all()
    post.increase_views()

    paginator = Paginator(comment_list, 10)
    page = request.GET.get('page')

    #评论分页
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comment_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comment_list = paginator.page(paginator.num_pages)

    return render(request,'third/detail.html',context={'post':post,'user_email':user_email,'form':form,
                                                       'comment_list':comment_list})

##博客归档
def archives(request,year,month):
    user_email = request.COOKIES.get('user_email')
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month)
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'third/index.html',context={'user_email':user_email,'post_list':post_list})

def listall(request):
    user_email = request.COOKIES.get('user_email')
    post_list = Post.objects.all()
    return render(request, 'third/archives.html',context={'user_email':user_email,'post_list':post_list})

"""
def archives(request,year,month):
    user_email = request.COOKIES.get('user_email')
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month)
    return render(request, 'third/archives.html',context={'user_email':user_email,'post_list':post_list})
"""

##博客分类
def category(request,category_id):
    user_email = request.COOKIES.get('user_email')
    cate=get_object_or_404(Category,pk=category_id)
    post_list=Post.objects.filter(category=cate)
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'third/index.html',context={'user_email':user_email,'post_list':post_list})

##博客标签
def tag(request,tag_id):
    user_email = request.COOKIES.get('user_email')
    user_tag = get_object_or_404(Tag, pk=tag_id)
    post_list = Post.objects.filter(tags=user_tag)
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'third/index.html',context={'user_email':user_email,'post_list':post_list})


##博客评论
def post_comment(request,post_id):
    user_email = request.COOKIES.get('user_email')
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':

        form=CommentForm(request.POST)

        if user_email and form.is_valid():
            user_text = form.cleaned_data['text']
            Comment.objects.create(email=user_email, text=user_text,post_id=post.id)
            return redirect('third:detail',post_id=post.id)
        else:
            comment_list = post.comment_set.all()

            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                      }
        return render(request,'third/detail.html')

    return redirect('third:detail', post_id=post.id)

##博客搜索
def search(request):
    search_name=request.GET.get('search_i')
    user_email = request.COOKIES.get('user_email')
    errors=[]

    if not search_name:
        errors.append('请输入关键词')
        return render(request, 'third/index.html', {'errors': errors})


    post_list = Post.objects.filter(Q(title__icontains=search_name) | Q(content__icontains=search_name))
    if not post_list:
        errors.append('搜索结果为空')
        return render(request, 'third/index.html', {'errors': errors})

    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'third/index.html', context={'user_email': user_email, 'post_list': post_list,'search_name':search_name})

##测试
def test(request):
    msg = '<a href="哈哈哈" target="_blank">hello world</a>'
    send_mail('标题', '内容', 'python<django_tinyshu@163.com>',
              ['345870016@qq.com'],
              html_message=msg)
    return HttpResponse('ok')




