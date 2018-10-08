# Generated by Django 2.1.1 on 2018-10-03 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wqual', '0007_featurefactory_int_source_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureset',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='wqual.Source'),
        ),
    ]
