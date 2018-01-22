from django.contrib import admin

from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'mobile',
                    'idNo',
                    'licType',
                    'currentStage',
                    'enrollDate')


admin.site.register(Student, StudentAdmin)
