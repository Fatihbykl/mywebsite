from django.contrib import admin
from .models import kullaniciProfili, Roles
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class NewUserModel_inline(admin.StackedInline):
    model = Roles
    can_delete = False
    verbose_name_plural = "Diğer Özellikler"


class Useradmin(UserAdmin):
    inlines = (NewUserModel_inline,)


admin.site.unregister(User)
admin.site.register(User, Useradmin)
admin.site.register(kullaniciProfili)
