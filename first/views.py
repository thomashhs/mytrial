from django.shortcuts import render,get_object_or_404
from .models import Title
from django.http import HttpResponse
import math
from .forms import CompundForm,LoanForm,BmiForm,UploadForm
import os

# Create your views here.
def index(request):
    latest_title_list=Title.objects.order_by('title_date')[:5]
    return render(request,'first/index.html',context={'latest_title_list':latest_title_list})


def detail(request,title_id):
    title=get_object_or_404(Title,pk=title_id)
    if title.title_text=='复利计算器':
        form=CompundForm()
    if title.title_text=='住房贷款计算':
        form=LoanForm()
    if title.title_text=='BMI指数':
        form=BmiForm()
    if title.title_text=='文件上传':
        form=UploadForm()
        return render(request, 'first/detail_2.html', context={'title': title, 'form': form})
    return render(request, 'first/detail_1.html', context={'title': title, 'form': form})



def result(request,title_id):
    title = get_object_or_404(Title, pk=title_id)

    if title.title_text == '复利计算器':
        if request.method=='POST':
            form=CompundForm(request.POST)


            if form.is_valid():
                form=CompundForm(coupund_interest_calculate(form))
                return render(request, 'first/result_1.html', context={'title':title,
                                                               'form':form})

    if title.title_text == '住房贷款计算':
        if request.method == 'POST':
            form = LoanForm(request.POST)

            if form.is_valid():
                form = LoanForm(mortage_calculate(form))
                return render(request, 'first/result_1.html', context={'title': title,
                                                                       'form': form})

    if title.title_text == 'BMI指数':
        if request.method=='POST':
            form=BmiForm(request.POST)

            if form.is_valid():
                form=BmiForm(bmi_calculate(form))
                return render(request, 'first/result_1.html', context={'title':title,
                                                               'form':form})
    if title.title_text == '文件上传':
        if request.method=='POST':
            form=UploadForm(request.POST,request.FILES)

            if form.is_valid():
                file_name=request.FILES['file_upload'].name
                handle_uploaded_file(request.FILES['file_upload'])
                file_check(file_name)
           #     file_process(file_name)
                return render(request, 'first/result_1.html', context={'title': title,
                                                                       'form': form})


    return HttpResponse('fail')


#########函数定义区###########

###复利计算器
def coupund_interest_calculate(form):
    base_money = form.cleaned_data['base_money']
    base_rate = form.cleaned_data['base_rate'] / 100
    base_year = form.cleaned_data['base_year']

    result_money = base_money * pow((1 + base_rate), base_year)
    result_interest = result_money - base_money

    result_money = round(result_money, 2)
    result_interest = round(result_interest, 2)

    data = {
        'base_money': base_money,
        'base_rate': str(base_rate * 100) + '%',
        'base_year': base_year,
        'result_money': result_money,
        'result_interest': result_interest
    }
    return data

###住房贷款计算
def mortage_calculate(form):
    loan_type = form.cleaned_data['loan_type']
    loan_money = form.cleaned_data['loan_money']
    loan_rate = form.cleaned_data['loan_rate'] / 100 / 12
    loan_year = form.cleaned_data['loan_year']

    result_month = loan_year * 12

    if loan_type == '等额本息':
        result_avg_money = (loan_money * loan_rate * pow(1 + loan_rate, result_month)) / (
        pow(1 + loan_rate, result_month) - 1)
        result_total_money = result_avg_money * result_month
        result_interest = result_total_money - loan_money
        result_avg_money = round(result_avg_money, 2)
        result_total_money = round(result_total_money, 2)
        result_interest = round(result_interest, 2)

        data = {
            'loan_type': loan_type,
            'loan_money': loan_money,
            'loan_rate': str(round(loan_rate * 12 * 100, 3)) + '%',
            'loan_year': loan_year,
            'result_month': result_month,
            'result_avg_money': result_avg_money,
            'result_total_money': result_total_money,
            'result_interest': result_interest
        }
    elif loan_type == '等额本金':
        result_avg_money = (loan_money / result_month) + float(loan_money * loan_rate)
        result_interest = (1 + result_month) * loan_money * loan_rate / 2
        result_total_money = (1 + result_month) * loan_money * loan_rate / 2 + loan_money
        result_descending_money = loan_money / result_month * float(loan_rate)

        result_avg_money = round(result_avg_money, 2)
        result_total_money = round(result_total_money, 2)
        result_interest = round(result_interest, 2)
        result_descending_money = round(result_descending_money, 2)

        data = {
            'loan_type': loan_type,
            'loan_money': loan_money,
            'loan_rate': str(round(loan_rate * 12 * 100, 3)) + '%',
            'loan_year': loan_year,
            'result_month': result_month,
            'result_total_money': result_total_money,
            'result_avg_money': str(result_avg_money) + '  ' + '（首月后每月递减' + str(result_descending_money) + '）',
            'result_interest': result_interest
        }
    return data

###BMI指数
def bmi_calculate(form):
    bmi_height = form.cleaned_data['bmi_height'] / 100
    bmi_weight = form.cleaned_data['bmi_weight']
    bmi_result = float(bmi_weight) / (bmi_height * bmi_height)

    bmi_result = round(bmi_result, 2)
    print(bmi_result)
    if bmi_result < 18.5:
        bmi_conclusion = "偏瘦"
    elif bmi_result > 18.5 and bmi_result <= 23.9:
        bmi_conclusion = "正常"
    elif bmi_result >= 24:
        bmi_conclusion = "超重"

    data = {
        'bmi_height': bmi_height,
        'bmi_weight': bmi_weight,
        'bmi_result': bmi_result,
        'bmi_conclusion': bmi_conclusion,
    }
    return data

###文件上传
def handle_uploaded_file(f):
    with open('D:\\upload\\'+f.name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_check(file_name):
    if os.path.exists('D:\\upload\\' + file_name.strip('.txt') + '_test.txt'):
        os.remove('D:\\upload\\' + file_name.strip('.txt') + '_test.txt')

def file_process(file_name):
    with open('D:\\upload\\' + file_name) as f1:
        count = len(f1.readlines())
        f1.seek(0, os.SEEK_SET)
        for var in f1.readlines():
            if count == 1:
                var = "'" + var.strip() + "'"
            else:
                var = "'" + var.strip() + "'," + "\n"
            with open('D:\\upload\\' + file_name.strip('.txt') + '_test.txt', 'a') as f2:
                f2.write(var)
            count = count - 1