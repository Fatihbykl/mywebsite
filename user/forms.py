from django.contrib.auth.models import User
from django import forms
from .models import kullaniciProfili
from django.contrib.auth.forms import PasswordChangeForm
import datetime


class registerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Parola',
                               max_length=128,
                               min_length=8, required=True, help_text='Şifreniz en az 8 karakter olmalıdır')
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='Parola Tekrar', max_length=128,
        min_length=8, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(registerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['username'].widget.attrs = {'placeholder': 'Kullanıcı Adı', 'class': 'input-field',
                                                'style': 'margin:0;', 'onkeyup': 'validate_username_length()'}
        self.fields['email'].widget.attrs = {'placeholder': 'Email', 'class': 'input-field', 'style': 'margin:0;',
                                             'onkeyup': 'validate_email()'}
        self.fields['password'].widget.attrs = {'placeholder': 'Şifre', 'class': 'input-field', 'style': 'margin:0;'}
        self.fields['password_confirm'].widget.attrs = {'placeholder': 'Şifre Onay', 'class': 'input-field',
                                                        'style': 'margin:0;', 'onkeyup': 'validate_pass()'}

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password_confirm', 'Parolalar eşleşmiyor!')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email zaten kullanılıyor')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Kullanıcı adı kullanılıyor')
        elif len(username) < 8:
            raise forms.ValidationError("Kullanıcı adı en az 8 harf olmalı.")
        return username


class loginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Parola',
                               max_length=128,
                               min_length=8, required=True, help_text='Şifreniz en az 8 karakter olmalıdır')

    def __init__(self, *args, **kwargs):
        super(loginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'Kullanıcı Adı', 'class': 'input-field',
                                                'style': 'margin:0;'}
        self.fields['password'].widget.attrs = {'placeholder': 'Şifre', 'class': 'input-field', 'style': 'margin:0;'}

    class Meta:
        model = User
        fields = ['username', 'password']


YEARS = [i for i in range(1960, datetime.datetime.now().year)]


class profilModel(forms.ModelForm):
    dogum_gunu = forms.DateTimeField(widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = kullaniciProfili
        fields = ['ad', 'soyad', 'fav_film', 'fav_yonetmen', 'dogum_gunu']

    def __init__(self, *args, **kwargs):
        super(profilModel, self).__init__(*args, **kwargs)

        self.fields['ad'].widget.attrs = {'class': 'form-control', 'maxlength': '20'}
        self.fields['soyad'].widget.attrs = {'class': 'form-control', 'maxlength': '20'}
        self.fields['fav_film'].widget.attrs = {'class': 'form-control', 'maxlength': '200'}
        self.fields['fav_yonetmen'].widget.attrs = {'class': 'form-control', 'maxlength': '100'}
        self.fields['dogum_gunu'].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:5px;'}


class ChangePhotoForm(forms.ModelForm):
    class Meta:
        model = kullaniciProfili
        fields = ['profilFoto']


class PasswordChange(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChange, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs = {'class': 'form-control'}
        self.fields['new_password1'].widget.attrs = {'class': 'form-control'}
        self.fields['new_password2'].widget.attrs = {'class': 'form-control'}

    def clean_new_password1(self):
        pass1 = self.cleaned_data['new_password1']
        if len(pass1) < 8:
            raise forms.ValidationError('Yeni şifre en az 8 karakter olmak zorunda.')
        return pass1
