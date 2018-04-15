from django import forms
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget



class MeetingForm(forms.Form):
    func_type = forms.ChoiceField(label='功能号',
                                  choices=(('增加', '增加'),
                                           ('删除', '删除'),
                                           ('查询', '查询')),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    meeting_date = forms.DateField(label='会议日期',  required=False,
                                   input_formats=['%Y-%m-%d','%Y%m%d'],
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_time = forms.TimeField(label='起始时间', required=False,
                                 input_formats=['%H:%M:%S','%H:%M','%H'],
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    end_time = forms.TimeField(label='结束时间', required=False,
                               input_formats=['%H:%M:%S', '%H:%M', '%H'],
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    meeting_user = forms.CharField(label='预定人员',required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    meeting_content = forms.CharField(label='会议摘要',required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))