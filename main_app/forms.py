from django import forms
from .models import Posts, Comments, ContactUs


class PostsModel(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['baslik', 'icerik']

    def __init__(self, *args, **kwargs):
        super(PostsModel, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'text-style'}


class CommentModel(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['yorum']

    def __init__(self, *args, **kwargs):
        super(CommentModel, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'placeholder': 'Fikrini belirt...'}


class ContactForms(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['secenek', 'mesaj']

    def __init__(self, *args, **kwargs):
        super(ContactForms, self).__init__(*args, **kwargs)
        self.fields['secenek'].widget.attrs = {'class': 'form-control'}
        self.fields['mesaj'].widget.attrs = {'class': 'form-control',
                                             'style': 'resize:none;height:200px;margin-top:30px',
                                             'placeholder': 'Mesajınız'}
