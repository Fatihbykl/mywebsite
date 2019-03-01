from django.urls import path
from user.views import register, Login, profil, Logout

urlpatterns = [
    path('kayit-ol/', register, name='register'),
    path('giris-yap/', Login, name='login'),
    path('profil/<username>/', profil, name='profil'),
    path('cikis-yap/', Logout, name='logout'),
]