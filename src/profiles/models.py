
from django.db import models
from django.contrib.auth.models import User

from products.models import Product

# Create your models here.

class UserPurchase(models.Model):
    user = models.OneToOneField(User)
    products = models.ManyToManyField(Product)
    
    def __unicode__(self, ):
        return self.user.username
    
    