from django.urls import path
from main_app.views import post_views, post_create, post_detail, comment, like, report, that_movie, \
    follow, delete_post, edit_post, delete_comment, movie, search_movie, report_post

urlpatterns = [
    path('', post_views, name='gonderiler'),
    path('gonderi-olustur/', post_create, name='post-create'),
    path('film-ara/<movie_name>', search_movie, name="search-movie"),
    path('filmler/<imdb_id>/<movie_name>', movie, name="movie"),
    path('<slug>/', post_detail, name='post-detail'),
    path('yorum/<slug>/<sug_movie>/<movie_href>', comment, name='comment'),
    path('<slug>/<id>/begen', like, name="like"),
    path('<slug>/<id>/rapor_et', report, name="report"),
    path('<slug>/rapor_et', report_post, name="report-post"),
    path('<slug>/<id>/buldum', that_movie, name="that-movie"),
    path('<pk>/<slug>/yorum_sil', delete_comment, name='delete-comment'),
    path('<slug>/post_takip_et', follow, name="follow"),
    path('<slug>/gonderi_sil', delete_post, name='delete-post'),
    path('<slug>/gonderi-duzenle', edit_post, name='edit-post'),
]
