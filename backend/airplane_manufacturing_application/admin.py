from django.contrib import admin
from .models import Airplane, Part, Team, Employee

# Register your models here.
admin.site.register(Airplane)
admin.site.register(Part)
admin.site.register(Team)
admin.site.register(Employee)