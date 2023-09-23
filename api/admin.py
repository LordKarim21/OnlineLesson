from django.contrib import admin
from .models import Lesson, Product, Viewer


class ViewerAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_link', 'duration_seconds')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    filter_horizontal = ('lessons',)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Viewer, ViewerAdmin)
