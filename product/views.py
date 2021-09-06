from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Product, Image

# Create your views here.
class ProductDetailView(DetailView):
    template_name = "product/product_detail.html"

    def get_object(self):
        return get_object_or_404(Product, name=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img = Image.objects.filter(product=self.get_object())
        context["images"] = img
        return context

class ProductListView(ListView):
    template_name = "product/product_list.html"
    queryset = Product.objects.all()
