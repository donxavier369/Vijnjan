from django.contrib import admin
from .models import *
# Register your models here.

class ModulesInline(admin.StackedInline):
    model = Modules
    extra = 1

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'thumbnail', 'duration', 'tutor', 'is_trending', 'category')
    search_fields = ('name', 'description', 'tutor__username', 'category__name')
    list_filter = ('is_trending', 'category')
    inlines = [ModulesInline]

admin.site.register(Modules)  # If you want to manage Modules separately in the admin