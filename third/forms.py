from django import forms
from .models import Comment

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',"placeholder": "电子邮箱",}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "密码",}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "确认密码",}))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',"placeholder": "电子邮箱",}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "密码",}))

class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder": "电子邮箱", }))

class CommentForm(forms.Form):
    text=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',"placeholder": "添加评论",}))

class PasswordForm(forms.Form):
    password_origin = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "当前密码",}))
    password_new = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "新密码",}))
    password_verify = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',"placeholder": "新密码（重复）",}))