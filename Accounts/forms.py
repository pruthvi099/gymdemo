from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=256, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}) )
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg'}))

