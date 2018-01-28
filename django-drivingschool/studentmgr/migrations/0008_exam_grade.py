# Generated by Django 2.0.1 on 2018-01-28 03:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studentmgr', '0007_auto_20180126_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examDate', models.DateField(default=django.utils.timezone.now, verbose_name='考试时间')),
                ('subject', models.IntegerField(choices=[(0, '科目一'), (1, '科目二'), (2, '科目三'), (3, '科目四')], default=0, verbose_name='考试科目')),
                ('licType', models.IntegerField(choices=[(0, 'A1'), (1, 'A2'), (2, 'A3'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2'), (7, 'C3'), (8, 'C4'), (9, 'D'), (10, 'E'), (11, 'F'), (12, 'M'), (13, 'N'), (14, 'P')], default=5, verbose_name='驾照类型')),
                ('addr', models.CharField(blank=True, max_length=100, null=True, verbose_name='考试地点')),
                ('students', models.ManyToManyField(to='studentmgr.Student', verbose_name='考试学员')),
            ],
            options={
                'verbose_name': '考试',
                'verbose_name_plural': '考试',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hasPassed', models.BooleanField(default=True, verbose_name='是否通过')),
                ('score', models.CharField(blank=True, max_length=5, null=True, verbose_name='分数')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentmgr.Exam', verbose_name='考试')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentmgr.Student', verbose_name='学员')),
            ],
            options={
                'verbose_name': '成绩',
                'verbose_name_plural': '成绩',
            },
        ),
    ]