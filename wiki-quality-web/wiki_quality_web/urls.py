"""wiki_quality_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls import url

from wqual import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^publications$', views.PublicationList.as_view(), name='publications'),
    url(r'^featureSetConfigNew$', views.FeatureSetInsert.as_view(), name='feature_set_insert'),
    url(r'^featureSetConfigajaxNew$', views.FeatureSetInsertAJAX.as_view(), name='feature_set_insertAJAX'),
    url(r'^featureSetConfig/(?P<nam_feature_set>.*)/delete/$', views.FeatureSetDelete.as_view(), name='feature_set_delete'),
    url(r'^featureSetConfig/(?P<nam_feature_set>.*)$', views.FeatureSetEdit.as_view(), name='feature_set_edit'),
    url(r'^featureSetConfigajax$', views.FeatureSetEditAJAX.as_view(), name='feature_set_editAJAX'),
    url(r'^f(?P<nam_feature_set>.*)/insert_features/$', views.InsertUsedFeaturesView.as_view(), name='insert_used_features'),
    url(r'^getAllFeatures/(?P<nam_language>.*)$', views.ListFeaturesView.as_view(), name='list_all_features'),
    url(r'^featureSetConfig/(?P<nam_feature_set>[^#]*)#featuresEdit$', views.FeatureSetEdit.as_view(), name='feature_set_edit_features'),
    url(r'^insert_list_used_features.js', views.JSListAddUsedFeatureView.as_view(), name='insert_list_used_features'),
    url(r'^featureSetConfig$', views.FeatureSetListView.as_view(), name='feature_set_list'),
    url(r'^extractFeatures/(?P<id_dataset>.*)/delete/$', views.DatasetDelete.as_view(), name='dataset_delete'),
    url(r'^extractFeatures$', views.DatasetCreateView.as_view(), name='extract_features'),
    url(r'^extractFeatures/downloadResult/(?P<dataset_id>[0-9]+).(?P<format>(xls|json))$', views.DatasetDownloadView.as_view(), name="download_result"),
    url(r'^admin/', admin.site.urls),
    url(r'^publications$', views.PublicationList.as_view(), name='publications'),
    url(r'^usedFeatures/(?P<nam_feature_set>.*)$', views.UsedFeatureListView.as_view(), name='usedFeatures.js'),
    url(r'^usedFeatureIsConfigurable$', views.UsedFeatureIsConfigurableForm.as_view(), name='usedFeaturesIsConfigurableForm'),
    url(r'^used_features.js$', views.UsedFeatureListView.as_view(), name='used_feature_js'),
    url(r'^used_features.html', views.UsedFeatureListViewTeste.as_view(), name='used_features'),
    url(r'^$', auth_views.LoginView.as_view(template_name='content/home.html'), name="home"),
    url(r'^signup/', views.SignUpView.as_view(), name='signup'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^usedFeatureDelete$', views.UsedFeatureDelete.as_view(), name='usedFeaturesDelete'),

] 