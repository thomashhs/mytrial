from django.shortcuts import render,get_object_or_404
from .models import Title
from django.http import HttpResponse
import math
from .forms import CompundForm,LoanForm,BmiForm

# Create your views here.
def index(request):
    latest_title_list=Title.objects.order_by('title_date')[:5]
    return render(request,'first/index.html',context={'latest_title_list':latest_title_list})


def detail(request,title_id):
    title=get_object_or_404(Title,pk=title_id)
    if title.title_text=='复利计算器':
        form=CompundForm()
        return render(request, 'first/detail_1.html', context={'title': title,'form':form})
    if title.title_text=='住房贷款计算':
        form=LoanForm()
        return render(request, 'first/detail_1.html', context={'title': title, 'form': form})
    if title.title_text=='BMI指数':
        form=BmiForm()
        return render(request, 'first/detail_1.html', context={'title': title, 'form': form})
    return render(request,'first/detail.html',context={'title':title})



def result(request,title_id):
    title = get_object_or_404(Title, pk=title_id)

    if title.title_text == '复利计算器':
        if request.method=='POST':
            form=CompundForm(request.POST)


            if form.is_valid():
                base_money = form.cleaned_data['base_money']
                base_rate = form.cleaned_data['base_rate']/100
                base_year = form.cleaned_data['base_year']

                result_money = base_money*pow((1+base_rate),base_year)
                result_interest = result_money-base_money

                result_money=round(result_money,2)
                result_interest=round(result_interest,2)

                data={
                      'base_money':base_money,
                      'base_rate':str(base_rate*100)+'%',
                      'base_year':base_year,
                      'result_money':result_money,
                      'result_interest':result_interest
                     }
                form=CompundForm(data)

                return render(request, 'first/result_1.html', context={'title':title,
                                                               'form':form})

    if title.title_text == '住房贷款计算':
        if request.method == 'POST':
            form = LoanForm(request.POST)

            if form.is_valid():
                loan_type = form.cleaned_data['loan_type']
                loan_money = form.cleaned_data['loan_money']
                loan_rate = form.cleaned_data['loan_rate']/100/12
                loan_year = form.cleaned_data['loan_year']

                result_month = loan_year*12

                if loan_type=='等额本息':
                    result_avg_money = (loan_money*loan_rate*pow(1+loan_rate,result_month))/ (pow(1+loan_rate,result_month)-1)
                    result_total_money = result_avg_money*result_month
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
                elif loan_type=='等额本金':
                    result_avg_money = (loan_money/result_month)+float(loan_money*loan_rate)
                    result_interest = (1+result_month)*loan_money*loan_rate/2
                    result_total_money = (1+result_month)*loan_money*loan_rate/2+loan_money
                    result_descending_money = loan_money/result_month*float(loan_rate)

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
                        'result_avg_money': str(result_avg_money)+'  '+'（首月后每月递减'+str(result_descending_money)+'）',
                        'result_interest': result_interest
                    }

                form = LoanForm(data)
                return render(request, 'first/result_1.html', context={'title': title,
                                                                       'form': form})

    if title.title_text == 'BMI指数':
        if request.method=='POST':
            form=BmiForm(request.POST)

            if form.is_valid():
                bmi_height = form.cleaned_data['bmi_height']/100
                bmi_weight = form.cleaned_data['bmi_weight']
                bmi_result = float(bmi_weight)/(bmi_height*bmi_height)


                bmi_result=round(bmi_result,2)

                if bmi_result<18.5:
                    bmi_conclusion = "偏瘦"
                elif bmi_result>18.5 and bmi_result<=23.9:
                    bmi_conclusion = "正常"
                elif bmi_result>=24:
                    bmi_conclusion = "超重"

                data={
                      'bmi_height':bmi_height,
                      'bmi_weight':bmi_weight,
                      'bmi_result':bmi_result,
                      'bmi_conclusion':bmi_conclusion,
                     }

                form=BmiForm(data)

                return render(request, 'first/result_1.html', context={'title':title,
                                                               'form':form})

    return HttpResponse('fail')


