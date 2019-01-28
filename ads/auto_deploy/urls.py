from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'service', views.ServiceView)
router.register(r'department', views.DepartmentViewSet)
router.register(r'actions', views.ServiceActionsView)  # test
urlpatterns = [
    # url(r'^(?P<version>[v1|v2]+)/department/$', views.DepartmentView.as_view(), name='department'),
    url(r'^(?P<version>[v1|v2]+)/auth/$', views.AuthView.as_view(), name='auth'),
    url(r'^(?P<version>[v1|v2]+)/user/$', views.UserView.as_view({'get': 'list'})),
    url(r'^(?P<version>[v1|v2]+)/user/(?P<pk>\d+)/$', views.UserView.as_view({'get': 'retrieve'})),
    url(r'^(?P<version>[v1|v2]+)/script_editor/$', views.ActionsScriptsView.as_view({'get': 'list',
                                                                                           'post': 'create'})),
    url(r'^(?P<version>[v1|v2]+)/script_editor/(?P<pk>\d+)/$', views.ActionsScriptsView.as_view({
        'update': 'update', 'delete': 'destory', 'get': 'retrieve'})),
    url(r'^(?P<version>[v1|v2]+)/', include(router.urls))
]
