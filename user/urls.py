from django.urls import path, include
from user.views import register, Login, Logout, password_change,  profile_photo_change, \
    choose_photo

urlpatterns = [
    path('kayit-ol/', register, name='register'),
    path('giris-yap/', Login, name='login'),
    path('sifre-degistir/', password_change, name='passchange'),
    path('fotograf-yukle/<username>', profile_photo_change, name='change-photo'),
    path('fotograf-sec/<username>', choose_photo, name='choose-photo'),
    path('profil/<username>/', include('user.profile-tabs-url')),
    path('cikis-yap/', Logout, name='logout'),
]
