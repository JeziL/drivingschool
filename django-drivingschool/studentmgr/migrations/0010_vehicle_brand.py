# Generated by Django 2.0.1 on 2018-02-05 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentmgr', '0009_auto_20180205_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='brand',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='品牌型号'),
        ),
    ]
