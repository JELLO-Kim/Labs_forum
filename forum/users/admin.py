from django.contrib import admin

# Register your models here.

from users.models import User, UserType

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
admin.site.register(UserType, UserAdmin)