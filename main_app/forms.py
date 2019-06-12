from django import forms
from .models import Posts, Comments, ContactUs, Reports


class PostsModel(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['baslik', 'icerik']

    def __init__(self, *args, **kwargs):
        super(PostsModel, self).__init__(*args, **kwargs)
        self.fields['baslik'].widget.attrs = {'class': 'form-control', 'maxlength': '70',
                                              'style': 'margin-bottom:35px;'}
        self.fields['icerik'].widget.attrs = {'class': 'form-control', 'maxlength': '2278',
                                              'style': 'height:200px;margin-bottom:20px'}


class CommentModel(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['yorum']

    def __init__(self, *args, **kwargs):
        super(CommentModel, self).__init__(*args, **kwargs)
        self.fields['yorum'].widget.attrs = {'placeholder': 'Fikrini belirt...'}


class ContactForms(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['ad', 'soyad', 'email', 'secenek', 'mesaj']

    def __init__(self, *args, **kwargs):
        super(ContactForms, self).__init__(*args, **kwargs)
        self.fields['secenek'].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:30px'}
        self.fields['mesaj'].widget.attrs = {'class': 'form-control',
                                             'style': 'resize:none;height:200px;margin-bottom:30px',
                                             'placeholder': 'Mesajınız'}
        self.fields['ad'].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:30px'}
        self.fields['soyad'].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:30px'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:30px'}


class ReportForms(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ['reason', 'comment']

    def __init__(self, *args, **kwargs):
        super(ReportForms, self).__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs = {'class': 'form-control'}
        self.fields['comment'].widget.attrs = {'class': 'form-control',
                                               'style': 'resize:none;height:200px;margin-bottom:30px',
                                               'placeholder': 'Bu kullanıcıyı neden rapor ediyorsunuz?'}
