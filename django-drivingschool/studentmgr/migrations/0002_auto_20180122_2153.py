# Generated by Django 2.0.1 on 2018-01-22 13:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studentmgr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='渠道名称')),
                ('channelType', models.IntegerField(choices=[(0, '线下-门店直招'), (1, '线下-挂牌分校'), (2, '线下-内部职工'), (3, '线下-代理网点'), (4, '线上-营销活动'), (5, '线上-平台合作')], default=0, verbose_name='渠道类型')),
                ('addr', models.CharField(max_length=200, verbose_name='地址')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='ClassType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='班型名称')),
                ('licType', models.IntegerField(choices=[(0, 'A1'), (1, 'A2'), (2, 'A3'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2'), (7, 'C3'), (8, 'C4'), (9, 'D'), (10, 'E'), (11, 'F'), (12, 'M'), (13, 'N'), (14, 'P')], default=5, verbose_name='驾照类型')),
                ('price', models.CharField(max_length=5, verbose_name='班型价格')),
                ('period', models.IntegerField(choices=[(0, '全周'), (1, '周一至周五'), (2, '周末')], default=0, verbose_name='学车时段')),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Enroller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('mobile', models.CharField(max_length=15, verbose_name='手机号')),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentmgr.Channel', verbose_name='渠道')),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='backupPhone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='备用电话'),
        ),
        migrations.AlterField(
            model_name='student',
            name='currentStage',
            field=models.IntegerField(choices=[(0, '准备报考'), (1, '科目一'), (2, '科目二'), (3, '科目三'), (4, '科目四'), (5, '拿证')], default=0, verbose_name='当前科目'),
        ),
        migrations.AlterField(
            model_name='student',
            name='licChangeDate',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='换证时间'),
        ),
        migrations.AlterField(
            model_name='student',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='student',
            name='origLicType',
            field=models.IntegerField(blank=True, choices=[(0, 'A1'), (1, 'A2'), (2, 'A3'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2'), (7, 'C3'), (8, 'C4'), (9, 'D'), (10, 'E'), (11, 'F'), (12, 'M'), (13, 'N'), (14, 'P')], default=0, null=True, verbose_name='原驾照类型'),
        ),
        migrations.AddField(
            model_name='student',
            name='classType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentmgr.ClassType', verbose_name='报名班型'),
        ),
        migrations.AddField(
            model_name='student',
            name='enroller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentmgr.Enroller', verbose_name='招生代表'),
        ),
    ]
