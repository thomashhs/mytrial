# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-20 04:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('third', '0005_auto_20180420_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tag',
            new_name='tags',
        ),
    ]
