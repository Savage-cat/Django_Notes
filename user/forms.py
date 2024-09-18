
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def get_user(self):
        return self.user

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = authenticate(self.request, username=username, password=password)
        if not self.user:
            raise ValidationError('неправильный логин или пароль')

        return self.cleaned_data
