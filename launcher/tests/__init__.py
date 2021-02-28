# TODO: this should be configured elsewhere
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clusters.settings')
django.setup()