from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()
    price = models.IntegerField()
    video = models.TextField(blank=True)

    def get_default_img(self):
        return Product.objects.get(id=self.id).product_image.filter(default=True).first()

    def get_absolute_url(self):
        return reverse("product:product detail", kwargs={"slug": self.name})

class Image(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to='product/')
    default = models.BooleanField(default=False)