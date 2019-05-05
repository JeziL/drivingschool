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


# 成绩模型内联于学员模型类
class GradeInlineStu(admin.TabularInline):
    model = Grade
    extra = 0
    readonly_fields = ('exam', )
    suit_classes = 'suit-tab suit-tab-gradeinstu'

    def has_add_permission(self, request):
        return False


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
                     'enroller__name',
                     'pyFirstLetters',
                     'pyFull')
    inlines = (FeeInlineAdmin, GradeInlineStu, )
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
        }),
    ]
    suit_form_tabs = (
        ('enroll', '报名'),
        ('fees', '交费'),
        ('gradeinstu', '成绩', )
    )

    # 用于显示渠道类型
    def channel_type(self, obj):
        if obj.enroller:
            if obj.enroller.channel:
                return obj.enroller.channel.get_channelType_display()
        return '-'
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


# 成绩模型内联管理类
class GradeInlineAdmin(admin.TabularInline):
    model = Grade
    extra = 0
    suit_classes = 'suit-tab suit-tab-grades'

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(GradeInlineAdmin, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student' and hasattr(self, 'parent_obj'):
            if hasattr(self.parent_obj, 'students'):
                kwargs['queryset'] = self.parent_obj.students
            else:
                kwargs['queryset'] = Student.objects.none()
        return super(GradeInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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
    filter_horizontal = ('students', )
    inlines = (GradeInlineAdmin, )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-exam', ),
            'fields': [
                'examDate',
                'subject',
                'licType',
                'addr',
                'students',
            ]
        }),
    ]
    suit_form_tabs = (
        ('exam', '考试信息'),
        ('grades', '成绩登记'),
    )

    # 用于获取参考人数
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = '参考人数'

    # 保存考试时，为每个学员创建对应的成绩对象
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.is_valid():
            exam = form.instance
            for stu in form.cleaned_data['students']:
                if Grade.objects.filter(exam=exam, student=stu).count() == 0:
                    grade = Grade(student=stu, exam=exam, hasPassed=True, score='')
                    grade.save()


# 成绩模型管理类
@admin.register(Grade)
class GradeAdmin(RelatedFieldAdmin):
    list_display = ('student_name',
                    'student_mobile',
                    'exam_licType',
                    'exam_subject',
                    'exam_examDate',
                    'hasPassed')
    list_filter = ('exam__examDate',
                   'exam__subject',
                   'exam__licType',
                   'hasPassed')
    suit_list_filter_horizontal = list_filter
    search_fields = ('student__name', )

    def has_add_permission(self, request):
        return False

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


# 教练模型管理类
@admin.register(Coach)
class CoachAdmin(RelatedFieldAdmin):
    list_display = ('name',
                    'sex',
                    'mobile')
    search_fields = ('name',
                     'mobile')
    list_filter = ()


# 车辆模型表单类
class VehicleForm(ModelForm):
    class Meta:
        widgets = {
            'note': AutosizedTextarea,
        }


# 车辆模型管理类
@admin.register(Vehicle)
class VehicleAdmin(RelatedFieldAdmin):
    form = VehicleForm
    list_display = ('vid',
                    'vin',
                    'licId',
                    'brand',
                    'use',
                    'name')
    list_filter = ('use', )
    suit_list_filter_horizontal = list_filter
    search_fields = ('vid',
                     'licId')


# 油气模型管理类
@admin.register(Fuel)
class FuelAdmin(RelatedFieldAdmin):
    list_display = ('veh_licId',
                    'fType',
                    'coach_name',
                    'money',
                    'createDate')
    search_fields = ('veh__licId', )
    list_filter = ('fType',
                   'createDate',
                   'coach__name',
                   'veh__licId')
    suit_list_filter_horizontal = list_filter

    # 用于获取车辆和教练相关信息
    def veh_licId(self, obj):
        return obj.veh.licId

    def coach_name(self, obj):
        return obj.coach.name

    veh_licId.short_description = '车牌号'
    coach_name.short_description = '上报教练'


# 维修模型表单类
class MaintenanceForm(ModelForm):
    class Meta:
        widgets = {
            'note': AutosizedTextarea,
        }


# 维修模型管理类
@admin.register(Maintenance)
class MaintenanceAdmin(RelatedFieldAdmin):
    form = MaintenanceForm
    list_display = ('veh_licId',
                    'coach_name',
                    'note',
                    'money',
                    'createDate')
    search_fields = ('veh__licId', )
    list_filter = ('createDate', )
    suit_list_filter_horizontal = list_filter

    # 用于获取车辆和教练相关信息
    def veh_licId(self, obj):
        return obj.veh.licId

    def coach_name(self, obj):
        return obj.coach.name

    veh_licId.short_description = '车牌号'
    coach_name.short_description = '上报教练'


# 保险模型管理类
@admin.register(Insurance)
class InsuranceAdmin(RelatedFieldAdmin):
    list_display = ('veh_licId',
                    'company',
                    'insType',
                    'money',
                    'startDate',
                    'endDate',
                    'createDate')
    search_fields = ('veh__licId', )
    list_filter = ('createDate', )
    suit_list_filter_horizontal = list_filter

    # 用于获取车辆和教练相关信息
    def veh_licId(self, obj):
        return obj.veh.licId

    veh_licId.short_description = '车牌号'


# 年审模型管理类
@admin.register(Examination)
class ExaminationAdmin(RelatedFieldAdmin):
    list_display = ('veh_licId',
                    'createDate',
                    'startDate',
                    'endDate')
    search_fields = ('veh__licId', )
    list_filter = ('createDate', )
    suit_list_filter_horizontal = list_filter

    # 用于获取车辆和教练相关信息
    def veh_licId(self, obj):
        return obj.veh.licId

    veh_licId.short_description = '车牌号'
