from django import forms

class CompundForm(forms.Form):
    base_money=forms.IntegerField(label='本金')
    base_rate=forms.DecimalField(label='年利率')
    base_year=forms.IntegerField(label='年期')