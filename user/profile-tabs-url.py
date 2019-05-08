from django.urls import path
from user.views import profile_settings, profile_info, my_posts, profile_notifications, bookmarks

urlpatterns = [
    path('profili-duzenle/', profile_settings, name='settings'),
    path('bilgiler/', profile_info, name='profile-info'),
    path('gonderiler/', my_posts, name='my-posts'),
    path('bildirimler/', profile_notifications, name='profile-notifications'),
    path('takip-ettiklerim/', bookmarks, name="bookmarks"),
]