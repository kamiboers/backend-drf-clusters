from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from launcher import views


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('clusters/', views.cluster_list),
    path('clusters/<int:pk>/', views.cluster_detail),
    path('auth/', views.authenticate),
    path('admin/', admin.site.urls),
]
