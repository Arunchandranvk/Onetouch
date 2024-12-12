from django.contrib import admin
from .models import *
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5  

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name',)
    inlines = [ProductImageInline]


admin.site.register(Categories)