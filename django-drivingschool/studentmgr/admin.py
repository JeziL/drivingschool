from django.contrib import admin
from .models import Student, ClassType, Enroller, Channel


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'mobile',
                    'idNo',
                    'licType',
                    'classType',
                    'currentStage',
                    'channel_type',
                    'enroller',
                    'enrollDate')
    list_filter = ('enrollDate',
                   'licType',
                   'classType',
                   'currentStage',
                   'enroller__channel__channelType')
    search_fields = ('name',
                     'mobile',
                     'idNo',
                     'enroller__name')

    # 用于显示渠道类型
    def channel_type(self, obj):
        return obj.enroller.channel.get_channelType_display()
    channel_type.short_description = '渠道类型'


class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'licType',
                    'price',
                    'period',
                    'createTime')
    list_filter = ('licType',
                   'period')
    search_fields = ('name', )


class EnrollerAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'mobile',
                    'channel')
    list_filter = ('channel', )
    search_fields = ('name',
                     'mobile')


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'channelType',
                    'addr',
                    'createTime')
    list_filter = ('createTime',
                   'channelType')
    search_fields = ('name', )


admin.site.register(Student, StudentAdmin)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(Enroller, EnrollerAdmin)
admin.site.register(Channel, ChannelAdmin)
