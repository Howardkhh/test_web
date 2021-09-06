from django.contrib import admin
from django.db import models
from .models import Product, Image

# Register your models here.

class ImageAdmin(admin.StackedInline):
    model = Image

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
        model = Product

# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     pass