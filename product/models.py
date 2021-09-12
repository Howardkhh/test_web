from mysite.settings import MEDIA_ROOT
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image as PIL_Image
import os

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

@receiver(pre_save, sender=Image)
def crop_img(sender, instance, *args, **kwargs):
    if instance.image:
        img = PIL_Image.open(instance.image)
        w, h = img.width, img.height
        ratio = 16/9
        if w/h > ratio:
            img = img.crop((int((w-h*ratio)/2), 0, int(h*ratio), h))
        elif w/h < ratio:
            img = img.crop((0, int((h-w/ratio)/2), w, int(w/ratio)))
        img.save(os.path.join(MEDIA_ROOT, 'product/' + instance.name + '.jpg'))
        instance.image = 'product/' + instance.name + '.jpg'