from django.shortcuts import render
from django.views.generic import ListView
from product.models import Product

# Create your views here.
class MenuView(ListView):
    template_name = "menu/menu.html"
    queryset = Product.objects.all()