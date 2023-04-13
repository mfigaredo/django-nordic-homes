from django.db import models
from django.utils.text import slugify
from django.contrib.humanize.templatetags.humanize import intcomma
from PIL import Image
from io import BytesIO
from django.core.files import File

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)

  class Meta:
    ordering = ('name', )
    verbose_name_plural = 'Categories'
  
  def __str__(self):
    return self.name

class Product(models.Model):
  category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  
  description = models.TextField(blank=True, null=True)
  price = models.IntegerField()  # in cents

  image = models.ImageField(upload_to='uploads/', blank=True, null=True)
  thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('-created_at', )

  def __str__(self):
    return self.name
  
  def get_display_price(self):
    return self.price / 100.00

  def get_thumbnail(self):
    if self.thumbnail:
      return self.thumbnail.url
    else:
      if self.image:
        self.thumbnail = self.make_thumbnail(self.image)
        self.save()
        return self.thumbnail.url
      else:
        return 'https://via.placeholder.com/240x200.jpg'
  
  def make_thumbnail(self, image, size=(240,200)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)
    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name.split('/')[-1])

    return thumbnail