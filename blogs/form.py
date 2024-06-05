from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=24)
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False,
                            widget=forms.Textarea) 

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username=forms.CharField(label='username',max_length=100)
    email=forms.EmailField(label="Email",max_length=264)
    password=forms.CharField(label="password",widget=forms.PasswordInput)