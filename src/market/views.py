import os
from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, HttpResponse


from cart.models import Cart
from products.models import Featured



def home(request):
    featured_products = []
    
    featured = Featured.objects.get_featured_instance()
    for i in featured.products.all():
        featured_products.append(i)
        
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = False
        cartitems = None
        
    if cart:
        cartitems = []
        for item in cart.cartitem_set.all():
            cartitems.append(item.product)

    return render_to_response("home.html", locals(), context_instance=RequestContext(request))
