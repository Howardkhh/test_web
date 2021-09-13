from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from PIL import Image as PIL_Image
from io import BytesIO

# Create your models here.
class Product(models.Model):
    name = models.CharField("商品名稱", max_length=100)
    detail = models.TextField("商品描述")
    price = models.IntegerField("價格")
    thumbnail = models.ImageField("商品圖像", upload_to='product/')
    video = models.TextField("介紹影片", blank=True)

    def __str__(self):
        return "product " + self.name

    def get_absolute_url(self):
        return reverse("product:product detail", kwargs={"slug": self.name})

    class Meta:
        
        verbose_name = "商品"
        verbose_name_plural = "商品"

class Image(models.Model):
    name = models.CharField("照片名稱", max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField("照片檔案", upload_to='product/')

    
    def __str__(self) -> str:
        return self.name

@receiver(pre_save, sender=Product)
def crop_img(sender, instance, *args, **kwargs):
    if instance.thumbnail:
        img = PIL_Image.open(instance.thumbnail)
        w, h = img.width, img.height
        ratio = 1
        if w/h > ratio:
            img = img.crop((int((w-h*ratio)/2), 0, int((w-h*ratio)/2)+int(h*ratio), h))
        elif w/h < ratio:
            img = img.crop((0, int((h-w/ratio)/2), w, int((h-w/ratio)/2)+int(w/ratio)))
        img = img.resize((480, 480))
        img_io = BytesIO()
        img.save(img_io, "JPEG", quality=50)
        instance.thumbnail = File(img_io, name=f'{instance.name}/thumbnail/{instance.name}_thumbnail.jpg')

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
        img.save(img_io, "JPEG", quality=80)
        instance.image = File(img_io, name=f'{instance.product.name}/product_images/{instance.name}.jpg')

