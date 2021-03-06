# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beltexamapp', '0003_auto_20160822_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traveler',
            name='user_id',
        ),
        migrations.AddField(
            model_name='traveler',
            name='traveler',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='beltexamapp.User'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='traveler',
            name='creators',
            field=models.ManyToManyField(related_name='creator', to='beltexamapp.User'),
        ),
    ]
