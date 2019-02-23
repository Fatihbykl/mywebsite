from django.urls import path
from user.views import register, loginn

urlpatterns = [
    path('kayit-ol/', register, name='register'),
    path('giris-yap/', loginn, name='login'),
]