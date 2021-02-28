from django.contrib import admin

from .models import Cluster, User


admin.site.register(Cluster)
admin.site.register(User)