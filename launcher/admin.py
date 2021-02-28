from django.contrib import admin

from .models import User
from clusters.models import Cluster


admin.site.register(Cluster)
admin.site.register(User)
