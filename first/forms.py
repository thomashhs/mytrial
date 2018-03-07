from django import forms

class CompundForm(forms.Form):
    base_money=forms.IntegerField(label='本金')
    base_rate=forms.DecimalField(label='年利率')
    base_year=forms.IntegerField(label='年期')

class LoanForm(forms.Form):
    loan_money=forms.IntegerField(label='贷款总额')
    loan_year=forms.IntegerField(label='贷款年限')
    loan_rate=forms.DecimalField(label='商贷利率')
