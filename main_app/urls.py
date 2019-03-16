from django.urls import path
from main_app.views import post_views, post_create, post_detail, comment, contact_us

urlpatterns = [
    path('', post_views, name='gonderiler'),
    path('gonderi-olustur/', post_create, name='post-create'),
    path('iletisim/', contact_us, name='contact'),
    path('<slug>/', post_detail, name='post-detail'),
    path('yorum/<slug>', comment, name='comment'),
]
