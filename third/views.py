from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from .forms import RegisterForm,LoginForm
from .models import User,Logacn,Logtxn,Test
from first.models import Title
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    user_email=request.COOKIES.get('user_email')
    if user_email:
        return render(request, 'third/login.html',context={'user_email':user_email})

    latest_title_list = Title.objects.order_by('title_date')[:5]
    return render(request, 'third/index.html',context={'latest_title_list':latest_title_list})

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

            response=render(request, 'third/login.html',context={'user_email':user_email})
            response.set_cookie('user_email',user_email,3600)
            return response
    else:
        form=LoginForm()
    return render(request, 'third/sign_in.html',context={'form':form})

def logout(request):
    response=render(request, 'third/index.html')
    response.delete_cookie('user_email')
    return response

def test(request):
    log_list = Logacn.objects.order_by('-pub_date')
    paginator = Paginator(log_list, 2)
    page = request.GET.get('page')

    try:
        log_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        log_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        log_list = paginator.page(paginator.num_pages)

    return render(request,'third/test.html',context={'log_list':log_list})