from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from main_app.models import Posts, Comments

def upload_to_directory(instance, filename):
    return 'avatar/%s/%s' % (instance.id, filename)


class kullaniciProfili(models.Model):
    k_adi2 = models.CharField(max_length=30, editable=False, default=1)
    profil = models.OneToOneField(User, null=True, on_delete=True, related_name='profil')
    ad = models.CharField(blank=True, max_length=30)
    soyad = models.CharField(blank=True, max_length=30)
    profilFoto = models.ImageField(upload_to=upload_to_directory, default="martian.jpg", blank=True)
    puan = models.IntegerField(editable=False, default=0)
    fav_film = models.CharField(max_length=250, blank=True)
    fav_yonetmen = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Kullanıcı Profilleri'

    def __str__(self):
        return '%s' % self.k_adi2

    def post_count(self):
        count = Posts.objects.filter(yayinlayan=self.profil).count()
        return count

    def comment_count(self):
        count = Comments.objects.filter(k_adi=self.profil.username).count()
        return count

class PasswordChange(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChange, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'textprofil'}
