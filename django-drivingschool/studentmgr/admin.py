from django.contrib import admin
from suit.admin import RelatedFieldAdmin
from .models import Student, ClassType, Enroller, Channel


# 学员模型管理类
@admin.register(Student)
class StudentAdmin(RelatedFieldAdmin):
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
    suit_list_filter_horizontal = list_filter
    search_fields = ('name',
                     'mobile',
                     'idNo',
                     'enroller__name')

    # 用于显示渠道类型
    def channel_type(self, obj):
        return obj.enroller.channel.get_channelType_display()
    channel_type.short_description = '渠道类型'


# 班型模型管理类
@admin.register(ClassType)
class ClassTypeAdmin(RelatedFieldAdmin):
    list_display = ('name',
                    'licType',
                    'price',
                    'period',
                    'createTime')
    list_filter = ('licType',
                   'period')
    suit_list_filter_horizontal = list_filter
    search_fields = ('name', )


# 招生代表模型内联管理类
class EnrollerInlineAdmin(admin.TabularInline):
    model = Enroller
    extra = 0


# 渠道模型管理类
@admin.register(Channel)
class ChannelAdmin(RelatedFieldAdmin):
    list_display = ('name',
                    'channelType',
                    'addr',
                    'createTime')
    list_filter = ('createTime',
                   'channelType')
    suit_list_filter_horizontal = list_filter
    search_fields = ('name', )
    inlines = (EnrollerInlineAdmin, )
