from django.contrib import admin
from models import *

admin.site.register(Sponsor)
admin.site.root_path = "/admin/"
