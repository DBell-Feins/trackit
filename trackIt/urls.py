from django.conf.urls import patterns, include, url
from common.api import UserResource, GoalResource, WeighInResource
from tastypie.api import Api
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(GoalResource())
v1_api.register(WeighInResource())

urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # API
    url(r'^api/', include(v1_api.urls)),
)
