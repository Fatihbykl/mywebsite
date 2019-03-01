from django import forms
from .models import Posts


class PostsModel(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['baslik', 'icerik']

    def __init__(self, *args, **kwargs):
        super(PostsModel, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'text-style'}
