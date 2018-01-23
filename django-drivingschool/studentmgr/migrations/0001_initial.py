# Generated by Django 2.0.1 on 2018-01-22 12:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
                ('idNo', models.CharField(max_length=20, verbose_name='证件号')),
                ('region', models.IntegerField(choices=[(0, '本地'), (1, '外地')], default=0, verbose_name='地域')),
                ('mobile', models.CharField(max_length=15, verbose_name='手机号')),
                ('backupPhone', models.CharField(max_length=15, verbose_name='备用电话')),
                ('addr', models.CharField(max_length=200, verbose_name='住址')),
                ('licType', models.IntegerField(choices=[(0, 'A1'), (1, 'A2'), (2, 'A3'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2'), (7, 'C3'), (8, 'C4'), (9, 'D'), (10, 'E'), (11, 'F'), (12, 'M'), (13, 'N'), (14, 'P')], default=5, verbose_name='驾照类型')),
                ('applyType', models.IntegerField(choices=[(0, '初领'), (1, '增驾')], default=0, verbose_name='申请方式')),
                ('origLicType', models.IntegerField(choices=[(0, 'A1'), (1, 'A2'), (2, 'A3'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2'), (7, 'C3'), (8, 'C4'), (9, 'D'), (10, 'E'), (11, 'F'), (12, 'M'), (13, 'N'), (14, 'P')], verbose_name='原驾照类型')),
                ('licChangeDate', models.DateField(verbose_name='换证时间')),
                ('currentStage', models.IntegerField(choices=[(0, '准备报考'), (1, '科目一'), (2, '科目二'), (3, '科目三'), (4, '科目四'), (5, '拿证')], verbose_name='当前科目')),
                ('enrollDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='报名时间')),
                ('note', models.TextField(verbose_name='备注')),
            ],
        ),
    ]