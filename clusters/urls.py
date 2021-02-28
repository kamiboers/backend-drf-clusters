from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from launcher import views


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('clusters/<int:pk>/', views.cluster_detail),
    path('clusters/', views.cluster_list),
    path('auth/', auth_views.obtain_auth_token),
    path('admin/', admin.site.urls),
]
