from django import forms
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget



class MeetingForm(forms.Form):
    func_type = forms.ChoiceField(label='功能号', choices=(('增加', '增加'), ('删除', '删除'),('修改', '修改'),('查询', '查询')))
    meeting_date = forms.DateField(label='会议日期',widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    start_time = forms.TimeField(label='起始时间', widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    end_time = forms.TimeField(label='结束时间', widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    meeting_user = forms.CharField(label='预定人员',required=False)
    meeting_content = forms.CharField(label='会议摘要',required=False)