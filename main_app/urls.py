from django.urls import path
from main_app.views import post_views, post_create, post_detail, comment, contact_us, like, report, that_movie, report_post, follow

urlpatterns = [
    path('', post_views, name='gonderiler'),
    path('gonderi-olustur/', post_create, name='post-create'),
    path('iletisim/', contact_us, name='contact'),
    path('<slug>/', post_detail, name='post-detail'),
    path('yorum/<slug>', comment, name='comment'),
    path('<slug>/<id>/begen', like, name="like"),
    path('<slug>/<id>/rapor_et', report, name="report"),
    path('<slug>/<id>/buldum', that_movie, name="that-movie"),
    path('<slug>/post_rapor_et', report_post, name="report-post"),
    path('<slug>/post_takip_et', follow, name="follow"),

]
