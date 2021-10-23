from django import forms
from .models import LoginForm

class SigninForm(forms.ModelForm):

    class Meta:
        model = LoginForm
        fields = ('username','password')
        labels = {
            'username':'Username',
            'password':'Password'
        }
        
def __init__(self, *args, **kwargs):
    super(Signinform,self).__init__(*args, **kwargs)
