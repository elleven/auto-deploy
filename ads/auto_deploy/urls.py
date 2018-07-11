from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/department/$', views.DepartmentView.as_view(), name='department'),
    url(r'^(?P<version>[v1|v2]+)/auth/$', views.AuthView.as_view(), name='auth'),
]
