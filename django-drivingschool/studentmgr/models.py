from django.db import models
from django.utils import timezone
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
    name = models.CharField('姓名', max_length=20)
    sex = models.IntegerField('性别', choices=SEX_OPTIONS, default=0)
    idNo = models.CharField('证件号', max_length=20)
    region = models.IntegerField('地域', choices=REGION_OPTIONS, default=0)
    mobile = models.CharField('手机号', max_length=15)
    backupPhone = models.CharField('备用电话', max_length=15, null=True, blank=True)
    addr = models.CharField('住址', max_length=200)
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
    feeId = models.CharField('编号', max_length=15, default=increment_fee_id, editable=False)
    createTime = models.DateTimeField('登记时间', default=timezone.now)

    def __str__(self):
        return self.feeId
