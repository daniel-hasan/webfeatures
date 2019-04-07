'''
Created on 07 de abr de 2019
Cria automaticamente todos os elementos dos feature factory graph
@author: Isabela Costa Souza <isabela.costasouza10@gmail.com>
'''

from django.db import migrations
namModuleFeatureFactory = "feature.feature_factory.feature_factory"
def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    FeatureFactory = apps.get_model("wqual", "FeatureFactory")
    db_alias = schema_editor.connection.alias
    
    FeatureFactory.objects.using(db_alias).bulk_create([
        FeatureFactory(nam_module=namModuleFeatureFactory,nam_factory_class="GraphFeatureFactory"),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    FeatureFactory = apps.get_model("wqual", "FeatureFactory")
    db_alias = schema_editor.connection.alias
    FeatureFactory.objects.using(db_alias).filter(nam_module=namModuleFeatureFactory,nam_factory_class="GraphFeatureFactory").delete()

class Migration(migrations.Migration):

    dependencies = [('wqual', '0009_merge_20181217_1659'),]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]