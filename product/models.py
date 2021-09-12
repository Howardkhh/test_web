from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.dispatch import receiver
from PIL import Image as PIL_Image
import os
from io import BytesIO

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, *args, **kwargs):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()
    price = models.IntegerField()
    video = models.TextField(blank=True)

    def __str__(self):
        return "product " + self.name

    def get_default_img(self):
        return Product.objects.get(id=self.id).product_image.filter(default=True).first()

    def get_absolute_url(self):
        return reverse("product:product detail", kwargs={"slug": self.name})

class Image(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to='product/'+product.name)
    default = models.BooleanField(default=False)

@receiver(pre_save, sender=Image)
def crop_img(sender, instance, *args, **kwargs):
    if instance.image:
        img = PIL_Image.open(instance.image)
        w, h = img.width, img.height
        ratio = 4/3
        if w/h > ratio:
            img = img.crop((int((w-h*ratio)/2), 0, int((w-h*ratio)/2)+int(h*ratio), h))
        elif w/h < ratio:
            img = img.crop((0, int((h-w/ratio)/2), w, int((h-w/ratio)/2)+int(w/ratio)))
        if img.width > 1920:
            img = img.resize((1920, 1440))
        img_io = BytesIO()
        img.save(img_io, "JPEG", quality=60)
        instance.image = File(img_io, name=instance.name+'.jpg')

