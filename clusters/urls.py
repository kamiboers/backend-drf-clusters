from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers

from launcher import views


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.authtoken')),
    path('clusters/', views.cluster_list),
    path('clusters/<int:pk>/', views.cluster_detail),
    path('admin/', admin.site.urls),
]
