from django.contrib import admin
from .models import Student, ClassType, Enroller, Channel


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'mobile',
                    'idNo',
                    'licType',
                    'classType',
                    'currentStage',
                    'enroller',
                    'enrollDate')


class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'licType',
                    'price',
                    'period',
                    'createTime')


class EnrollerAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'mobile',
                    'channel')


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'channelType',
                    'addr',
                    'createTime')


admin.site.register(Student, StudentAdmin)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(Enroller, EnrollerAdmin)
admin.site.register(Channel, ChannelAdmin)
