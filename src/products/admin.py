from django.contrib import admin

from .models import Product, Category, ProductImage, Tag, CategoryImage, Featured

class FeaturedProductsAdmin(admin.ModelAdmin):
    class Meta:
        model = Featured
        
admin.site.register(Featured, FeaturedProductsAdmin)

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage

class TagInline(admin.TabularInline):
    prepopulated_fields = {"slug": ('tag',)}
    extra = 1
    model = Tag

    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    
    
class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__unicode__', 'description', 'current_price', 'order', 'categories', 'live_link',)
    inlines = [TagInline, ProductImageInline]
    search_fields = ['title', 'description', 'price', 'category__title', 'category__description', 'tag__tag']
    list_filter = ['price', 'sale_price', 'timestamp', 'updated']
    list_editable = ['description', 'order',]
    prepopulated_fields = {"slug": ('title',)}
    readonly_fields = ['categories', 'live_link', 'timestamp', 'updated',]
    
    class Meta:
        model = Product
       
        
    def current_price(self, obj):
        if obj.sale_price > 0:
            return obj.sale_price
        else:
            return obj.price

    def categories(self, obj):
        cat = []
        for i in obj.category_set.all():
            link = "<a href='/admin/products/category/"+ str(i.id) + "/'>" + i.title + "</a>"
            cat.append(link)
        return ", ".join(cat)
    
    categories.allow_tags = True
    
    def live_link(self, obj):
        link = "<a href='/products/"+ str(obj.slug) + "/'>" + obj.title + "</a>"
        return link
    
    live_link.allow_tags = True

admin.site.register(Product, ProductAdmin)


   
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    inlines = [CategoryImageInline]
    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)









