from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'profile_image', 'person', 'date_of_birth', 'gender', 'is_tutor_verify' )

admin.site.register(CustomUser, UserAdmin)


