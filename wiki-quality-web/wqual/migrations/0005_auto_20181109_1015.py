# Generated by Django 2.0 on 2018-11-09 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wqual', '0004_auto_20180629_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitteddataset',
            name='dataset',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wqual.Dataset'),
        ),
    ]
