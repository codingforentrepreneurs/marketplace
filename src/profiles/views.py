from django.conf import settings
from django.shortcuts import render, RequestContext, Http404, HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory

from .models import UserPurchase



def library(request):
    if request.user.is_authenticated():
    	try:
        	products = request.user.userpurchase.products.all()
        except:
        	products = None
        return render(request, "profiles/library.html", {"products": products })
    else:
        raise Http404