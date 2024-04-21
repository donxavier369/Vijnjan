from django.contrib import admin
from .models import *
# Register your models here.

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'carousel_image',)

admin.site.register(Carousel, CarouselAdmin)
