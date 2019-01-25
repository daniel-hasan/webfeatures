'''
Created on 26 de fev de 2018
Cria automaticamente todos os elementos dos feature factory
(Legibilidade, estrutura, estilo)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
'''
from django.db import migrations
namModuleFeatureFactory = "feature.feature_factory.feature_factory"
def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    FeatureFactory = apps.get_model("wqual", "FeatureFactory")
    db_alias = schema_editor.connection.alias
    
    FeatureFactory.objects.using(db_alias).bulk_create([
        FeatureFactory(nam_module=namModuleFeatureFactory,nam_factory_class="StructureFeatureFactory"),
        FeatureFactory(nam_module=namModuleFeatureFactory,nam_factory_class="StyleFeatureFactory"),
        FeatureFactory(nam_module=namModuleFeatureFactory,nam_factory_class="WordsFeatureFactory"),
        FeatureFactory(nam_module=namModuleFeatureFactory,nam_factory_class="ReadabilityFeatureFactory"),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    FeatureFactory = apps.get_model("wqual", "FeatureFactory")
    db_alias = schema_editor.connection.alias
    FeatureFactory.objects.using(db_alias).filter(nam_module=namModuleFeatureFactory,nam_factory_class="StructureFeatureFactory").delete()
    FeatureFactory.objects.using(db_alias).filter(nam_module=namModuleFeatureFactory,nam_factory_class="StyleFeatureFactory").delete()
    FeatureFactory.objects.using(db_alias).filter(nam_module=namModuleFeatureFactory,nam_factory_class="WordsFeatureFactory").delete()
    FeatureFactory.objects.using(db_alias).filter(nam_module=namModuleFeatureFactory,nam_factory_class="ReadabilityFeatureFactory").delete()

class Migration(migrations.Migration):

    dependencies = [('wqual', '0001_initial'),]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]