# Generated by Django 2.1.1 on 2018-10-03 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wqual', '0006_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurefactory',
            name='int_source_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wqual.Source'),
        ),
    ]
