from django.contrib import admin

from .models import UserPurchase


class UserPurchaseAdmin(admin.ModelAdmin):
    class Meta:
        model = UserPurchase
        
admin.site.register(UserPurchase, UserPurchaseAdmin)