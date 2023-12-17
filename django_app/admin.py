from django.contrib import admin

from .models import Units, Users, Jobs

admin.site.register(Users)
admin.site.register(Units)
admin.site.register(Jobs)