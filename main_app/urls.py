from django.urls import path
from main_app.views import post_views, post_create

urlpatterns = [
    path('', post_views, name='gonderiler'),
    path('gonderi-olustur/', post_create, name='post-create')
]
