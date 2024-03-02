from django.contrib import admin
from .models import Job,State,Industry

# Register your models here.
admin.site.register(Job)
admin.site.register(State)
admin.site.register(Industry)