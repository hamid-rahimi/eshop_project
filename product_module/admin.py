from django.contrib import admin
from .models import Product, ProductCategory, ProductTag, Brand, ProductGallery


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_title', 'is_active')
    list_editable = ['is_active']
    list_filter = ('is_active', 'is_delete')
    search_fields = ('title',)
    
    class Meta:
        pass
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active', 'slug')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title',)
    prepopulated_fields = {'slug':['title']}
    
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ("id", "caption")

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(Brand)
admin.site.register(ProductGallery)