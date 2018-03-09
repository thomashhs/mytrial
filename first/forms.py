from django import forms

class CompundForm(forms.Form):
    base_money = forms.IntegerField(label='本金（元）',initial=100000)
    base_rate = forms.DecimalField(label='年利率（%）',initial=10)
    base_year = forms.IntegerField(label='年期（年）',initial=60)
    result_money = forms.CharField(label='本息合计（元）',required=False,initial='不需要填写')
    result_interest = forms.CharField(label='其中利息（元）',required=False,initial='不需要填写')

class LoanForm(forms.Form):
    loan_type = forms.ChoiceField(label='还款方式',choices = (('等额本息','等额本息'),('等额本金','等额本金'),))
    loan_money = forms.IntegerField(label='贷款总额（元）',initial=1170000)
    loan_year = forms.IntegerField(label='贷款年限（年）',initial=30)
    loan_rate = forms.DecimalField(label='商贷利率（%）',initial=4.41)
    result_month = forms.CharField(label='贷款月数（月）', required=False, initial='不需要填写')
    result_avg_money = forms.CharField(label='月均还款（元）', required=False, initial='不需要填写')
    result_total_money = forms.CharField(label='还款总额（元）', required=False, initial='不需要填写')
    result_interest = forms.CharField(label='支付利息（元）', required=False, initial='不需要填写')

class BmiForm(forms.Form):
    bmi_height = forms.IntegerField(label='身高（厘米）',initial=176)
    bmi_weight = forms.DecimalField(label='体重（公斤）',initial=65)
    bmi_result = forms.CharField(label='BMI指数',required=False,initial='不需要填写')
    bmi_conclusion = forms.CharField(label='结论',required=False,initial='不需要填写')

class UploadForm(forms.Form):
    file_upload=forms.FileField(label='文件上传处理')