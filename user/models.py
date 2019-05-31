from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import now
from main_app.models import Posts, Comments
import uuid
import datetime
from io import BytesIO
from PIL import Image
import sys


def upload_to_directory(instance, filename):
    return 'user_uploaded_images/%s/%s' % (instance.profil.username, filename)


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
        (6, 'Admin'),
        (7, 'Usta'),
    )
    user = models.OneToOneField(User, related_name='role_user', on_delete=models.CASCADE, default=uuid.uuid1)
    role = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    puan = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Kullanıcı Ayarları"

    def __str__(self):
        return "Kullanıcı Adı : %s , Puanı : %s , Seviyesi : %s" % (
            self.user.username, self.puan, self.get_role_display())

    def check_role(self):
        if not self.role == 6:
            if self.puan < 20:
                self.role = 1
            elif self.puan < 70:
                self.role = 2
            elif self.puan < 200:
                self.role = 3
            elif self.puan < 500:
                self.role = 4
            elif self.puan < 1000:
                self.role = 5
            else:
                self.role = 7

    def get_leaderboard_full(self):
        points = Roles.objects.all()
        list = []
        for i in points:
            list.append(i.puan)

        list.sort(reverse=True)

        obj_list = []
        for j in list:
            obj_list.append(Roles.objects.filter(puan=j))
        return obj_list

    def get_leaderboard_5(self):
        return self.get_leaderboard_full()[:5]

    def get_user_place(self, user):
        place = Roles.objects.get(user=user)
        return place


class kullaniciProfili(models.Model):
    CHOOSE = (
        (1, 'default_avatars/avatar.jpg'),
        (2, 'default_avatars/javier.jpg'),
        (3, 'default_avatars/joker.png'),
        (4, 'default_avatars/pennywise.jpg'),
        (5, 'default_avatars/scarface.jpg'),
        (6, 'default_avatars/unknown.jpg'),
        (7, 'default_avatars/yoda.jpg'),
    )

    k_adi2 = models.CharField(max_length=30, editable=False, default=1)
    profil = models.OneToOneField(User, default=uuid.uuid1, on_delete=models.CASCADE, related_name='profil')
    ad = models.CharField(blank=True, max_length=30)
    soyad = models.CharField(blank=True, max_length=30)
    profilFoto = models.ImageField(upload_to=upload_to_directory, default="icons/indir.png", blank=True)
    fav_film = models.CharField(max_length=250, blank=True)
    fav_yonetmen = models.CharField(max_length=50, blank=True)
    dogum_gunu = models.DateField(default=now())
    cinsiyet = models.CharField(max_length=10, default='?', blank=True)
    buldugu_film = models.IntegerField(default=0)
    date_joined = models.DateField(default=now())
    choose_photo = models.PositiveSmallIntegerField(choices=CHOOSE, blank=True, default=1)

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

    def get_age(self):
        today = datetime.datetime.now()
        birthday = self.dogum_gunu
        age = today.year - birthday.year
        if today.month < birthday.month:
            age -= 1
        elif today.month == birthday.month and today.day < birthday.day:
            age -= 1
        return age

    def get_cinsiyet_display(self):
        if self.cinsiyet == 'erkek':
            return 'Erkek'
        elif self.cinsiyet == 'kadin':
            return 'Kadın'
