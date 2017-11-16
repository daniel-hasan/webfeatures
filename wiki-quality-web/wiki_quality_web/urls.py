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
from django.conf.urls import url
from django.contrib import admin

from wqual import views


urlpatterns = [
    url(r'^featureSetConfigNew$', views.FeatureSetInsert.as_view(), name='feature_set_insert'),
    url(r'^featureSetConfig/(?P<nam_feature_set>.*)$', views.FeatureSetEdit.as_view(), name='feature_set_edit'),
    url(r'^featureSetConfig$', views.FeatureSetListView.as_view(), name='feature_set_list'),
    url(r'^extractFeatures$', views.DatasetListView.as_view(), name='extract_features'),
    url(r'^admin/', admin.site.urls),
    url(r'^publications$', views.PublicationList.as_view(), name='publications'),
    url(r'^used_features.js$', views.UsedFeatureListView.as_view(), name='used_feature_js'),
    url(r'^used_features.html', views.UsedFeatureListViewTeste.as_view(), name='used_features'),
]
