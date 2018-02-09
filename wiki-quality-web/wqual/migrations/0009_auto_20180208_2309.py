# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-08 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wqual', '0008_remove_documentresult_dsc_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedfeatureargval',
            name='type_argument',
            field=models.CharField(choices=[('int', 'int'), ('float', 'float'), ('string', 'string'), ('boolean', 'boolean'), ('json', 'json'), ('json_set', 'json_set')], default='string', max_length=10),
        ),
        migrations.AlterField(
            model_name='usedfeatureargval',
            name='val_argument',
            field=models.CharField(max_length=5000),
        ),
    ]
