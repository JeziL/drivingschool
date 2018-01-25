from django.contrib import admin
from django.forms import ModelForm
from suit.admin import RelatedFieldAdmin
from suit.widgets import AutosizedTextarea
from .models import Student, ClassType, Enroller, Channel, Fee


# 页面标题
admin.site.site_header = '鸿铭驾校管理系统'


# 学员模型表单类
class StudentForm(ModelForm):
    class Meta:
        widgets = {
            'addr': AutosizedTextarea,
            'note': AutosizedTextarea,
        }

    class Media:
        js = (
            'admin/js/jquery-3.3.1.min.js',
            'admin/js/student_detail.js',
        )


# 费用模型内联管理类
class FeeInlineAdmin(admin.StackedInline):
    model = Fee
    extra = 0
    suit_classes = 'suit-tab suit-tab-fees'


# 学员模型管理类
@admin.register(Student)
class StudentAdmin(RelatedFieldAdmin):
    form = StudentForm
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
    inlines = (FeeInlineAdmin, )
    readonly_fields = ('class_type_price', )
    fieldsets = [
        ('个人信息', {
            'classes': ('suit-tab suit-tab-enroll', ),
            'fields': [
                'name',
                'sex',
                'idNo',
                'region',
                'mobile',
                'backupPhone',
                'addr',
            ]
        }),
        ('报名信息', {
            'classes': ('suit-tab suit-tab-enroll', ),
            'fields': [
                'licType',
                'applyType',
                'origLicType',
                'licChangeDate',
                'classType',
                'enroller',
                'currentStage',
                'enrollDate',
            ]
        }),
        ('其他信息', {
            'classes': ('suit-tab suit-tab-enroll', ),
            'fields': [
                'note',
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-fees', ),
            'fields': [
                'class_type_price',
            ]
        })
    ]
    suit_form_tabs = (
        ('enroll', '报名'),
        ('fees', '交费'),
    )

    # 用于显示渠道类型
    def channel_type(self, obj):
        return obj.enroller.channel.get_channelType_display()
    channel_type.short_description = '渠道类型'

    # 用于显示班型价格
    def class_type_price(self, obj):
        return obj.classType.price
    class_type_price.short_description = '班型价格'


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


# 费用模型管理类
@admin.register(Fee)
class FeeAdmin(RelatedFieldAdmin):
    list_display = ('feeId',
                    'student_name',
                    'student_mobile',
                    'student_idNo',
                    'student_enroller_name',
                    'student_licType',
                    'student_classType',
                    'feeType',
                    'money',
                    'createTime')
    list_filter = ('createTime',
                   'student__licType',
                   'student__classType',
                   'feeType')
    suit_list_filter_horizontal = list_filter
    search_fields = ('student__name',
                     'student__mobile',
                     'student__idNo',
                     'student__enroller__name')

    # 用于获取学员相关信息
    def student_name(self, obj):
        return obj.student.name

    def student_mobile(self, obj):
        return obj.student.mobile

    def student_idNo(self, obj):
        return obj.student.idNo

    def student_enroller_name(self, obj):
        return obj.student.enroller.name

    def student_licType(self, obj):
        return obj.student.get_licType_display()

    def student_classType(self, obj):
        return obj.student.classType.name

    student_name.short_description = '学员姓名'
    student_mobile.short_description = '手机号'
    student_idNo.short_description = '证件号'
    student_enroller_name.short_description = '招生代表'
    student_licType.short_description = '驾照类型'
    student_classType.short_description = '班型'
