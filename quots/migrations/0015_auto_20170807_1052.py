# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-07 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quots', '0014_out_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='in',
            name='jumun',
            field=models.CharField(max_length=200, verbose_name='키워드명'),
        ),
        migrations.AlterField(
            model_name='in',
            name='many',
            field=models.IntegerField(default=0, verbose_name='가격'),
        ),
        migrations.AlterField(
            model_name='out',
            name='ans_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='1순위결정날짜'),
        ),
        migrations.AlterField(
            model_name='out',
            name='dapbyun',
            field=models.CharField(max_length=200, verbose_name='상호명'),
        ),
        migrations.AlterField(
            model_name='out',
            name='inflag',
            field=models.BooleanField(default=False, verbose_name='노출1순위'),
        ),
    ]
