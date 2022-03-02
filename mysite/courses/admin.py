from django.contrib import admin

from . import models


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'published_at')


# Register your models here.
admin.site.register(models.Teacher)
admin.site.register(models.Course, admin_class=CourseAdmin)
admin.site.register(models.Review)
