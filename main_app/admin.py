from django.contrib import admin
from .models import Posts, Comments, ContactUs, Reports

admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(ContactUs)
admin.site.register(Reports)
