from django.db import models
from django.utils import timezone

SEX_OPTIONS = (
    (0, '男'),
    (1, '女'),
)
REGION_OPTIONS = (
    (0, '本地'),
    (1, '外地'),
)
LICENSE_TYPE_OPTIONS = (
    (0, 'A1'),
    (1, 'A2'),
    (2, 'A3'),
    (3, 'B1'),
    (4, 'B2'),
    (5, 'C1'),
    (6, 'C2'),
    (7, 'C3'),
    (8, 'C4'),
    (9,  'D'),
    (10, 'E'),
    (11, 'F'),
    (12, 'M'),
    (13, 'N'),
    (14, 'P'),
)
APPLY_TYPE_OPTIONS = (
    (0, '初领'),
    (1, '增驾'),
)
STAGE_OPTIONS = (
    (0, '准备报考'),
    (1, '科目一'),
    (2, '科目二'),
    (3, '科目三'),
    (4, '科目四'),
    (5, '拿证'),
)


class Student(models.Model):
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


