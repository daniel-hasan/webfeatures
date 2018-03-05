# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-04 22:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_first', models.CharField(max_length=50)),
                ('nam_middle', models.CharField(max_length=50)),
                ('nam_last', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_conference', models.CharField(max_length=255)),
                ('nam_abbreviation', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_dataset', models.CharField(max_length=45)),
                ('dat_submitted', models.DateTimeField()),
                ('dat_valid_until', models.DateTimeField(blank=True, null=True)),
                ('bol_ready_to_process', models.BooleanField(default=False)),
                ('start_dat_processing', models.DateTimeField(blank=True, null=True)),
                ('end_dat_processing', models.DateTimeField(blank=True, null=True)),
                ('dsc_result_header', django_mysql.models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_file', models.CharField(blank=True, max_length=255, null=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wqual.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsc_result', django_mysql.models.JSONField(default=dict)),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wqual.Document')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsc_text_bin', models.BinaryField()),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wqual.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_module', models.CharField(max_length=45)),
                ('nam_feature_class', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureConfigurableParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_feature', models.CharField(max_length=45)),
                ('dsc_feature', models.CharField(max_length=255)),
                ('dsc_arr_choices', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'wqual_feature_configurable_param',
            },
        ),
        migrations.CreateModel(
            name='FeatureFactory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_module', models.CharField(max_length=45)),
                ('nam_factory_class', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'wqual_feature_factory',
            },
        ),
        migrations.CreateModel(
            name='FeatureSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_feature_set', models.CharField(max_length=50)),
                ('dsc_feature_set', models.CharField(blank=True, max_length=255, null=True)),
                ('bol_is_public', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'wqual_feature_set',
            },
        ),
        migrations.CreateModel(
            name='FeatureTimePerDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeatureVisibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_machine', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParamType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessingDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_proc_extractor', models.IntegerField()),
                ('dataset', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='wqual.Dataset')),
                ('machine_extractor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_title', models.CharField(max_length=400)),
                ('num_year', models.IntegerField()),
                ('authors', models.ManyToManyField(to='wqual.Author')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='ResultValityPerUserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_days_valid', models.IntegerField()),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UsedFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ord_feature', models.IntegerField()),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Feature')),
                ('feature_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wqual.FeatureSet')),
                ('feature_time_to_extract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.FeatureTimePerDocument')),
                ('feature_visibility', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.FeatureVisibility')),
                ('text_format', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Format')),
            ],
            options={
                'db_table': 'wqual_used_feature',
            },
        ),
        migrations.CreateModel(
            name='UsedFeatureArgVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nam_argument', models.CharField(blank=True, max_length=45, null=True)),
                ('nam_att_argument', models.CharField(max_length=60)),
                ('val_argument', models.CharField(max_length=5000)),
                ('dsc_argument', models.CharField(blank=True, max_length=255, null=True)),
                ('json_choices', django_mysql.models.JSONField(blank=True, default=dict, null=True)),
                ('type_argument', models.CharField(choices=[('int', 'int'), ('float', 'float'), ('string', 'string'), ('boolean', 'boolean'), ('json', 'json'), ('json_set', 'json_set')], default='string', max_length=10)),
                ('is_configurable', models.BooleanField(default=False)),
                ('used_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wqual.UsedFeature')),
            ],
        ),
        migrations.AddField(
            model_name='featureset',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Language'),
        ),
        migrations.AddField(
            model_name='featureset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='featureconfigurableparam',
            name='param_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wqual.ParamType'),
        ),
        migrations.AddField(
            model_name='featureconfigurableparam',
            name='used_feature',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='wqual.UsedFeatureArgVal'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='feature_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.FeatureSet'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='format',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Format'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wqual.Status'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='featureset',
            index=models.Index(fields=['nam_feature_set', 'user'], name='wqual_featu_nam_fea_46fef1_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='featureset',
            unique_together=set([('nam_feature_set', 'user')]),
        ),
    ]
