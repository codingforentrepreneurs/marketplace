import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

protected_loc = settings.PROTECTED_UPLOADS





def download_loc(instance, filename):
    if instance.user.username:
        return "%s/download/%s" %(instance.user.username, filename)
    else:
        return "%s/download/%s" %("default", filename)

class Product(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=180)
    description = models.CharField(max_length=500)
    download = models.FileField(upload_to=download_loc, storage=FileSystemStorage(location=protected_loc), null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-order']
        
    def get_price(self):
        if self.sale_price > 0:
            return self.sale_price
        else:
            return self.price
    
    def get_featured_image(self):
        try:
            images = self.productimage_set.all()
        except:
            return None
        
        for i in images:
            if i.featured_image:
                return i.image
            else:
                return None


    def is_active(self):
        return self.active
        
    def get_absolute_url(self, ):
        return reverse('single_product', args=[self.slug])
    
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to="products/image/")
    title = models.CharField(max_length=120, null=True, blank=True)
    featured_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return str(self.title)
    

    
class Tag(models.Model):
    product = models.ForeignKey(Product)
    tag = models.CharField(max_length=20)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return str(self.tag)


class Category(models.Model):
    products = models.ManyToManyField(Product)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def get_absolute_url(self, ):
        return reverse('category', args=[self.slug])


class CategoryImage(models.Model):
    category = models.ForeignKey(Category)
    image = models.ImageField(upload_to="products/image/")
    title = models.CharField(max_length=120, null=True, blank=True)
    featured_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Category Image"
        verbose_name_plural = "Category Images"

class FeaturedManager(models.Manager):
    def get_featured_instance(self):
        items = super(FeaturedManager, self).filter(date_start__lte=datetime.datetime.now()).filter(date_end__gte=datetime.datetime.now())
        all_items = super(FeaturedManager, self).all()
        if len(items) >= 1:
            return items[0]
        else:
            for i in all_items:
                if i.default:
                    return i
            return all_items[0]


class Featured(models.Model):
    title = models.CharField(max_length=120)
    products = models.ManyToManyField(Product, limit_choices_to={'active': True}, null=True, blank=True)
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    date_end = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    default = models.BooleanField(default=False)
    jumbo_text = models.CharField(max_length=3000, null=True, blank=True)

    def __unicode__(self):
        return self.title
    
    def get_featured(self):
        return self.products[:2]

    objects = FeaturedManager()
    