from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Title,Meeting
from .forms import MeetingForm
from django.db.models import Q
import datetime

# Create your views here.
def index(request):
    latest_title_list = Title.objects.order_by('title_date')[:5]
    return render(request, 'second/index.html', context={'latest_title_list': latest_title_list})

def detail(request,title_id):
    title=get_object_or_404(Title,pk=title_id)
    if title.title_text=='会议记录':
        form=MeetingForm()
    return render(request, 'second/detail_1.html', context={'title': title, 'form': form})

def result(request,title_id):
    title = get_object_or_404(Title, pk=title_id)

    if title.title_text == '会议记录':
        if request.method=='POST':
            form=MeetingForm(request.POST)

            if form.is_valid():
                meeting_date = form.cleaned_data['meeting_date']
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']
                meeting_user = form.cleaned_data['meeting_user']
                meeting_content = form.cleaned_data['meeting_content']

                if meeting_date is not None and start_time is not None and end_time is not None:
                    meeting_start_date = datetime.datetime(year=meeting_date.year, month=meeting_date.month,
                                                           day=meeting_date.day,
                                                           hour=start_time.hour, minute=start_time.minute)
                    meeting_end_date = datetime.datetime(year=meeting_date.year, month=meeting_date.month,
                                                         day=meeting_date.day,
                                                         hour=end_time.hour, minute=end_time.minute)
                if meeting_date is not None and (start_time is None or end_time is None):
                    meeting_start_date = datetime.datetime(year=meeting_date.year, month=meeting_date.month,
                                                           day=meeting_date.day,
                                                           hour=0, minute=0)
                    meeting_end_date = datetime.datetime(year=meeting_date.year, month=meeting_date.month,
                                                         day=meeting_date.day,
                                                         hour=23, minute=0)
                if form.cleaned_data['func_type']=='增加':
                   if meeting_date and start_time and end_time and meeting_user and meeting_content:
                       if ( Meeting.objects.filter( Q(start_date__lte=meeting_start_date),
                                                    Q(end_date__gte=meeting_start_date)) or
                            Meeting.objects.filter( Q(start_date__lte=meeting_end_date),
                                                    Q(end_date__gte=meeting_end_date ))):
                           error_message = "该日程时间段已有人预定"
                           return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                               'error_message': error_message})

                       else:
                           meeting_list = Meeting(start_date=meeting_start_date, end_date=meeting_end_date,
                                                  meeting_user=meeting_user,
                                                  meeting_content=meeting_content)
                           meeting_list.save()
                           meeting_start_date = datetime.datetime(year=meeting_date.year, month=meeting_date.month,
                                                                  day=meeting_date.day,
                                                                  hour=0, minute=0)
                           meeting_end_date = datetime.datetime(year=meeting_date.year, month=meeting_date.month,
                                                                day=meeting_date.day,
                                                                hour=23, minute=0)
                           meeting_list = Meeting.objects.filter(Q(start_date__gte=meeting_start_date),
                                                                 Q(end_date__lte=meeting_end_date))

                           return render(request, 'second/result_2.html',
                                         context={'title': title, 'meeting_list': meeting_list})
                   else:
                       error_message = "选项必须全部输入"
                       return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                               'error_message': error_message})


                if form.cleaned_data['func_type']=='查询':

                    if meeting_date is None and start_time is None and end_time is None:
                        ###查询7天以内的记录
                        meeting_start_date=datetime.datetime.now()
                        meeting_end_date=meeting_start_date+datetime.timedelta(days=7)
                        meeting_list=Meeting.objects.filter(Q(start_date__gte=meeting_start_date),Q(end_date__lte=meeting_end_date))

                        if meeting_list:
                            return render(request, 'second/result_2.html',
                                          context={'title': title, 'meeting_list': meeting_list})
                        else:
                            error_message = "该查询结果为空"
                            return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                                    'error_message': error_message})
                    if meeting_date is not None and (start_time is None and end_time is None):
                        ###查询当天的记录
                        meeting_list = Meeting.objects.filter(Q(start_date__gte=meeting_start_date),
                                                              Q(end_date__lte=meeting_end_date))
                        if meeting_list:
                            return render(request, 'second/result_2.html',
                                          context={'title': title, 'meeting_list': meeting_list})
                        else:
                            error_message = "该查询结果为空"
                            return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                                    'error_message': error_message})
                    if meeting_date and start_time and end_time:
                        ###查询当天时间区间内的记录
                        meeting_list = Meeting.objects.filter(Q(start_date__gte=meeting_start_date),
                                                              Q(end_date__lte=meeting_end_date))
                        if meeting_list:
                            return render(request, 'second/result_2.html',
                                          context={'title': title, 'meeting_list': meeting_list})
                        else:
                            error_message = "该查询结果为空"
                            return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                                    'error_message': error_message})
                    if ((start_time is not None and end_time is None) or
                       (end_time is not None and start_time is None)):
                       error_message = '起始时间与结束时间必须都输入或不输入'
                       return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                               'error_message': error_message})

                if form.cleaned_data['func_type']=='删除':
                    if meeting_date is None:
                        error_message = "会议日期必须输入"
                        return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                                'error_message': error_message})
                    if (start_time and end_time) or (start_time is None and end_time is None):
                        meeting_list = Meeting.objects.filter(Q(start_date__gte=meeting_start_date),
                                                              Q(end_date__lte=meeting_end_date))
                        if meeting_list:
                         #  meeting_list=meeting_list.delete()
                           return render(request, 'second/result_3.html',
                                          context={'title': title, 'meeting_list': meeting_list})
                        else:
                            error_message = "未查询到当天会议记录"
                            return render(request, 'second/detail_1.html', context={'title': title, 'form': form,
                                                                                    'error_message': error_message})
                    else:
                        error_message = "起始日期与结束日期必须同时输入或为空"
                        return render(request, 'second/detail_1.html', context={'title': title, 'form': form,

                                                                                'error_message': error_message})

def delete(request,title_id,meeting_id):
    meeting=get_object_or_404(Meeting,pk=meeting_id)
    title = get_object_or_404(Title, pk=title_id)
    meeting_list = meeting.delete()
    return render(request, 'second/delete_1.html',context={'title': title})