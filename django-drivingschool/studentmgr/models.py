from django.db import models
from django.utils import timezone
from django.utils.formats import date_format
from pypinyin import pinyin, lazy_pinyin, Style
from .options import *


# 渠道模型类
class Channel(models.Model):
    class Meta:
        verbose_name = '渠道'
        verbose_name_plural = '渠道'
    name = models.CharField('渠道名称', max_length=20)
    channelType = models.IntegerField('渠道类型', choices=CHANNEL_TYPE_OPTIONS, default=0)
    addr = models.CharField('地址', max_length=200)
    note = models.TextField('备注', null=True, blank=True)
    createTime = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.name


# 招生代表模型类
class Enroller(models.Model):
    class Meta:
        verbose_name = '招生代表'
        verbose_name_plural = '招生代表'
    name = models.CharField('姓名', max_length=20)
    mobile = models.CharField('手机号', max_length=15)
    channel = models.ForeignKey(Channel, verbose_name='渠道', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# 班型模型类
class ClassType(models.Model):
    class Meta:
        verbose_name = '班型'
        verbose_name_plural = '班型'
    name = models.CharField('班型名称', max_length=20)
    licType = models.IntegerField('驾照类型', choices=LICENSE_TYPE_OPTIONS, default=5)
    price = models.CharField('班型价格', max_length=10)
    period = models.IntegerField('学车时段', choices=PERIOD_OPTIONS, default=0)
    createTime = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.name


# 学员模型类
class Student(models.Model):
    class Meta:
        verbose_name = '学员'
        verbose_name_plural = '学员'
        ordering = ('-id', )
    name = models.CharField('姓名', max_length=20)
    pyFirstLetters = models.CharField('拼音首字母', max_length=20, null=True, blank=True)
    pyFull = models.CharField('全拼', max_length=100, null=True, blank=True)
    sex = models.IntegerField('性别', choices=SEX_OPTIONS, default=0)
    idNo = models.CharField('证件号', max_length=20)
    region = models.IntegerField('地域', choices=REGION_OPTIONS, default=0)
    mobile = models.CharField('手机号', max_length=15)
    backupPhone = models.CharField('备用电话', max_length=15, null=True, blank=True)
    addr = models.CharField('住址', max_length=200, null=True, blank=True)
    licType = models.IntegerField('驾照类型', choices=LICENSE_TYPE_OPTIONS, default=5)
    applyType = models.IntegerField('申请方式', choices=APPLY_TYPE_OPTIONS, default=0)
    origLicType = models.IntegerField('原驾照类型', choices=LICENSE_TYPE_OPTIONS, default=0, null=True, blank=True)
    licChangeDate = models.DateField('换证时间', default=timezone.now, null=True, blank=True)
    currentStage = models.IntegerField('当前科目', choices=STAGE_OPTIONS, default=0)
    enrollDate = models.DateTimeField('报名时间', default=timezone.now)
    note = models.TextField('备注', null=True, blank=True)
    classType = models.ForeignKey(ClassType, verbose_name='报名班型', null=True, on_delete=models.SET_NULL)
    enroller = models.ForeignKey(Enroller, verbose_name='招生代表', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pyFirstLetters = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER, errors='ignore'))
        self.pyFull = ''.join(lazy_pinyin(self.name, errors='ignore'))
        super().save(*args, **kwargs)


# 用于在创建时生成按日自增的费用编号
def increment_fee_id():
    prefix = 'FYBM'
    last_fee = Fee.objects.all().order_by('id').last()
    cur_date = timezone.localtime().strftime('%y%m%d')
    if not last_fee:
        return prefix + cur_date + '001'
    last_id = last_fee.feeId
    last_date = last_id[4:10]
    last_id_no = int(last_id[10:13])
    if last_date == cur_date:
        return prefix + cur_date + str(last_id_no + 1).zfill(3)
    else:
        return prefix + cur_date + '001'


# 费用模型类
class Fee(models.Model):
    class Meta:
        verbose_name = '交费记录'
        verbose_name_plural = '交费记录'
    student = models.ForeignKey(Student, verbose_name='交费学员', on_delete=models.CASCADE)
    feeType = models.IntegerField('交费类别', choices=FEE_TYPE_OPTIONS, default=0)
    note = models.CharField('备注', max_length=100, null=True, blank=True)
    money = models.CharField('收费金额', max_length=10)
    paymentMethod = models.IntegerField('付款方式', choices=PAYMENT_OPTIONS, default=0)
    feeId = models.CharField('编号', max_length=15, default=increment_fee_id, editable=False)
    createTime = models.DateTimeField('登记时间', default=timezone.now)

    def __str__(self):
        return self.feeId


# 考试模型类
class Exam(models.Model):
    class Meta:
        verbose_name = '考试'
        verbose_name_plural = '考试'
    examDate = models.DateField('考试时间', default=timezone.now)
    subject = models.IntegerField('考试科目', choices=SUBJECT_OPTIONS, default=0)
    licType = models.IntegerField('驾照类型', choices=LICENSE_TYPE_OPTIONS, default=5)
    addr = models.CharField('考试地点', max_length=100, null=True, blank=True)
    students = models.ManyToManyField(Student, verbose_name='考试学员')

    def __str__(self):
        return date_format(self.examDate, 'SHORT_DATE_FORMAT') + ' ' + self.get_subject_display()


# 成绩模型类
class Grade(models.Model):
    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩'
    student = models.ForeignKey(Student, verbose_name='学员', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, verbose_name='考试', on_delete=models.CASCADE)
    hasPassed = models.BooleanField(verbose_name='是否通过', default=True)
    score = models.CharField('分数', max_length=5, null=True, blank=True)

    def __str__(self):
        return self.student.name + ' ' + str(self.exam)


# 教练模型类
class Coach(models.Model):
    class Meta:
        verbose_name = '教练'
        verbose_name_plural = '教练'
    name = models.CharField('姓名', max_length=20)
    sex = models.IntegerField('性别', choices=SEX_OPTIONS, default=0)
    mobile = models.CharField('手机号', max_length=15, null=True, blank=True)
    idNo = models.CharField('证件号', max_length=20, null=True, blank=True)
    note = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return self.name


# 车辆模型类
class Vehicle(models.Model):
    class Meta:
        verbose_name = '车辆'
        verbose_name_plural = '车辆'
    brand = models.CharField('品牌型号', max_length=15, null=True, blank=True)
    vid = models.CharField('车辆编号', max_length=15)
    vin = models.CharField('车架号', max_length=20)
    licId = models.CharField('车牌号', max_length=10)
    licDate = models.DateField('上牌日期', default=timezone.now)
    use = models.IntegerField('车辆用途', choices=VEHICLE_USE_OPTIONS, default=0)
    name = models.CharField('车主姓名', max_length=20)
    tel = models.CharField('联系电话', max_length=20, null=True, blank=True)
    note = models.TextField('备注', null=True, blank=True)

    def __str__(self):
        return self.licId


# 油气模型类
class Fuel(models.Model):
    class Meta:
        verbose_name = '油气'
        verbose_name_plural = '油气'
    fType = models.IntegerField('类型', choices=FUEL_TYPE_OPTIONS, default=0)
    veh = models.ForeignKey(Vehicle, verbose_name='车辆', on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, verbose_name='上报教练', on_delete=models.CASCADE)
    money = models.CharField('金额', max_length=10)
    createDate = models.DateField('加油时间', default=timezone.now)

    def __str__(self):
        return date_format(self.createDate, 'SHORT_DATE_FORMAT') + ' ' + self.veh.licId


# 维修模型类
class Maintenance(models.Model):
    class Meta:
        verbose_name = '维修'
        verbose_name_plural = '维修'
    veh = models.ForeignKey(Vehicle, verbose_name='车辆', on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, verbose_name='上报教练', on_delete=models.CASCADE)
    money = models.CharField('维修费用', max_length=10)
    createDate = models.DateField('维修时间', default=timezone.now)
    note = models.TextField('维修说明', null=True, blank=True)

    def __str__(self):
        return date_format(self.createDate, 'SHORT_DATE_FORMAT') + ' ' + self.veh.licId


# 保险模型类
class Insurance(models.Model):
    class Meta:
        verbose_name = '保险'
        verbose_name_plural = '保险'
    veh = models.ForeignKey(Vehicle, verbose_name='车辆', on_delete=models.CASCADE)
    company = models.CharField('保险公司', max_length=20)
    insType = models.CharField('险种', max_length=20)
    money = models.CharField('保险金额', max_length=10)
    createDate = models.DateField('投保时间', default=timezone.now)
    startDate = models.DateField('生效时间', default=timezone.now)
    endDate = models.DateField('失效时间', default=timezone.now)

    def __str__(self):
        return date_format(self.createDate, 'SHORT_DATE_FORMAT') + ' ' + self.veh.licId


# 年审模型类
class Examination(models.Model):
    class Meta:
        verbose_name = '年审'
        verbose_name_plural = '年审'
    veh = models.ForeignKey(Vehicle, verbose_name='车辆', on_delete=models.CASCADE)
    createDate = models.DateField('审查日期', default=timezone.now)
    startDate = models.DateField('生效日期', default=timezone.now)
    endDate = models.DateField('失效日期', default=timezone.now)

    def __str__(self):
        return date_format(self.createDate, 'SHORT_DATE_FORMAT') + ' ' + self.veh.licId
