from django.contrib import admin
from django.db import models
from .models import Product, Image

# Register your models here.

class ImageAdmin(admin.StackedInline):
    model = Image
    verbose_name = "照片"
    verbose_name_plural = "商品照片"
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
        model = Product