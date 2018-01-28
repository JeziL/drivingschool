from django.contrib import admin
from django.forms import ModelForm
from suit.admin import RelatedFieldAdmin
from suit.widgets import AutosizedTextarea
from .models import *
from .actions import *


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
            'admin/js/jquery-migrate-1.4.1.min.js',
            'admin/js/jquery.jqprint-0.3.js',
        )
        css = {
            'all': (
                'admin/css/student_detail.css',
            )
        }


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
    list_editable = ('currentStage', )
    actions = (export_students_as_csv_action(), )
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
    actions = (export_fees_as_csv_action(), )
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


# 考试模型管理类
@admin.register(Exam)
class ExamAdmin(RelatedFieldAdmin):
    list_display = ('examDate',
                    'subject',
                    'licType',
                    'students_count',
                    'addr')
    list_filter = ('examDate',
                   'subject',
                   'licType')
    suit_list_filter_horizontal = list_filter
    search_fields = ('examDate', )

    # 用于获取参考人数
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = '参考人数'


# 成绩模型管理类
@admin.register(Grade)
class GradeAdmin(RelatedFieldAdmin):
    list_display = ('student_name',
                    'student_mobile',
                    'exam_licType',
                    'exam_subject',
                    'exam_examDate',
                    'hasPassed')

    # 用于获取学员和考试相关信息
    def student_name(self, obj):
        return obj.student.name

    def student_mobile(self, obj):
        return obj.student.mobile

    def exam_licType(self, obj):
        return obj.exam.get_licType_display()

    def exam_subject(self, obj):
        return obj.exam.get_subject_display()

    def exam_examDate(self, obj):
        return obj.exam.examDate

    student_name.short_description = '姓名'
    student_mobile.short_description = '手机号'
    exam_licType.short_description = '驾照类型'
    exam_subject.short_description = '考试科目'
    exam_examDate.short_description = '考试时间'
