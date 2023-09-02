from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label']