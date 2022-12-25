from django.contrib import admin
from .models import Newsblock, Source, User

# Register your models here.

from django import forms

@admin.register(Newsblock)
class PersonAdmin(admin.ModelAdmin):
    fields = ("title", "text")


# admin.site.register(Newsblock)
admin.site.register(Source)
admin.site.register(User)