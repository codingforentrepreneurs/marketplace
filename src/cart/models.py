from django.db import models
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

# Create your models here.
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    total = models.DecimalField(max_digits=50, default=0, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return str(self.id)
    
    '''
    def save(self, *args, **kwargs):
        #override the save function
        totals = [item.product.price for item in self.cartitem_set.all()]
        new_total = sum(totals)
        self.total = new_total
        super(Cart, self).save(*args, **kwargs)
        
        totals = []
        for item in self.cartitem_set.all():
            totals.append(item.product.price)
        '''

class CartItem(models.Model):
    cart = models.ForeignKey(Cart) #create cart model
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        return "%s" %(self.product.title)



@receiver([signals.post_save, signals.post_delete], sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart
    totals = [item.product.get_price() for item in cart.cartitem_set.all()]
    cart.total = sum(totals)
    cart.save()


