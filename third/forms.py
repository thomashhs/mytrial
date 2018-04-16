from django import forms

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',"placeholder": "电子邮箱",}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "密码",}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "确认密码",}))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',"placeholder": "电子邮箱",}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "密码",}))