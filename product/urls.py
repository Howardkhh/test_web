from django.urls import path
from product.views import *

app_name = "product"
urlpatterns = [
    path("", ProductListView.as_view(), name="product list"),
    path("<str:slug>", ProductDetailView.as_view(), name="product detail"),
]