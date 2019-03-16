from django.urls import path
from user.views import register, Login, profil, Logout, password_change, edit_profile

urlpatterns = [
    path('kayit-ol/', register, name='register'),
    path('giris-yap/', Login, name='login'),
    path('sifre-degistir/', password_change, name='passchange'),
    path('profil-duzenle/<username>', edit_profile, name='edit-profile'),
    path('profil/<username>/', profil, name='profil'),
    path('cikis-yap/', Logout, name='logout'),
]