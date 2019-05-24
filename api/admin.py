from django.contrib import admin

# Register your models here.
from .models import Company, Entry

admin.site.register(Company)
admin.site.register(Entry)
