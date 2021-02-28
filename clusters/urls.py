from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from launcher import views


router = routers.DefaultRouter()
router.register(r'clusters', views.ClusterViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
