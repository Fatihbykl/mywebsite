from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from main_app.models import Posts, Comments
import uuid


def upload_to_directory(instance, filename):
    return 'avatar/%s/%s' % (instance.id, filename)


class Roles(models.Model):
    yeni_uye = 1
    caylak = 2
    filmsever = 3
    film_uzmani = 4
    profesyonel = 5
    admin = 6
    ROLES = (
        (1, 'Yeni Üye'),
        (2, 'Çaylak'),
        (3, 'Filmsever'),
        (4, 'Film Uzmanı'),
        (5, 'Profesyonel'),
        (6, 'Admin')
    )
    user = models.OneToOneField(User, related_name='role_user', on_delete=models.CASCADE, default=uuid.uuid1)
    role = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    puan = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Kullanıcı Ayarları"

    def __str__(self):
        return "Puan ve Rütbe Bölümü"

    def check_role(self):
        if self.puan <= 5:
            self.role = 1
        elif self.puan <= 25:
            self.role = 2
        elif self.puan <= 50:
            self.role = 3
        elif self.puan <= 50:
            self.role = 4
        elif self.puan > 50:
            self.role = 5


class kullaniciProfili(models.Model):
    k_adi2 = models.CharField(max_length=30, editable=False, default=1)
    profil = models.OneToOneField(User, default=uuid.uuid1, on_delete=models.CASCADE, related_name='profil')
    ad = models.CharField(blank=True, max_length=30)
    soyad = models.CharField(blank=True, max_length=30)
    profilFoto = models.ImageField(upload_to=upload_to_directory, default="/icons/indir.png", blank=True)
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
