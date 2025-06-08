from users.models import CustomUser
from django.contrib import admin


@admin.register(CustomUser)
class AuthorAdmin(admin.ModelAdmin):
    exclude = ("password",)
