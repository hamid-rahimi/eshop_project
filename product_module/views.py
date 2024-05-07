from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.db.models import Avg, Count
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
)

from .models import Product, ProductCategory, Brand, ProductGallery
from home_module.models import AdvertisingBanner, MoreVisitedProduct
from tools.ip import get_client_ip_address
from tools.group_list import convert_to_group_list

class FavoriteProductListView(ListView):
    template_name = "product_module/favorite_product_list.html"
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        favorite_products = Product.objects.filter(favorite_product__user=user)
        context["products"] = favorite_products
        return context

"""
def products_list(request):
    all_products = Product.objects.all()
    number_of_products = all_products.count()
    price_average = all_products.aggregate(Avg("price"))
    
    return render(request, "product_module/products-list.html", {
        'products': all_products,
        'number_of_products': number_of_products,
        'price_average': price_average,
    })

class ProductListView(TemplateView):
    template_name = "product_module/products-list.html"
    
    products = Product.objects.all()
    products_count = products.count()
    price_average = products.aggregate(Avg('price'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        context['number_of_products'] = self.products_count
        context['price_average'] = self.price_average
        return context
"""
class ProductListView(ListView):
    model = Product
    template_name = "product_module/products-list.html"
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['price_average'] = Product.objects.aggregate(Avg('price'), Count('title'))
        return context

def product_detail(request: HttpRequest, slug):
    number_of_brands = Brand.objects.annotate(count=Count('products_brand'))
    product = get_object_or_404(Product, slug=slug)
    
    return render(request, "product_module/product-detail.html", {
        'product': product,
        'brands': number_of_brands,
    })
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_module/product-detail.html"
    context_object_name = 'product'
    query_pk_and_slug = True
    
    def get_queryset(self):
        is_visited = self.set_visited_product()
        print(f"is visited = {is_visited}")
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        loaded_product = self.object
        context = super().get_context_data(**kwargs)
        gallery = list(ProductGallery.objects.filter(product=loaded_product).all())
        gallery.insert(0, loaded_product )
        print(gallery)
        context["gallery"] = convert_to_group_list(gallery, 3)
        return context
    
    
    def set_visited_product(self) -> bool:
        ip = get_client_ip_address(self.request)
        product = Product.objects.filter(slug__iexact=self.kwargs['slug']).first()
        has_ip = MoreVisitedProduct.objects.filter(ip__iexact=ip, product__slug__iexact=product.slug).exists()
        
        if (product is not None) and (ip is not None) and (not has_ip):
            if self.request.user.is_authenticated:
                visited = MoreVisitedProduct(product=product, ip=ip, user=self.request.user)
            else:
                visited = MoreVisitedProduct(product=product, ip=ip)
            visited.save()
            return True 
            
        print(f"user={self.request.user}, ip={ip}, product={product}")
    

"""_summary_
def products_view(request):
    products = Product.objects.all()
    number_of_brands = Brand.objects.annotate(count=Count('products_brand'))
    return render(request, "product_module/products-page.html", {
        'products': products,
        'brands': number_of_brands,
    })"""
    

class ProductView(ListView):
    template_name = "product_module/products-page.html"
    model = Product
    context_object_name = 'products'
    paginate_by = 3
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['start_price'] = 5
    #     context['end_price'] = 1000000
    #     print('context')
    #     return context
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset()
        category_id = self.kwargs.get('cat_id')
        print(self.kwargs, self.request.GET)
        query = query.filter(is_active=True, is_delete=False)
        if category_id:
            query = query.filter(product_category__id=category_id)
        
        order_query_by_price = query.order_by('price')    
        min_price = 0
        max_price = order_query_by_price.last().price or 900000000  
        start_price = self.request.GET.get('start_price') or min_price
        end_price = self.request.GET.get('end_price') or max_price
        query = query.filter(price__gte=start_price)
        query = query.filter(price__lte=end_price)

        return query
    
            
def sidebar_loader(request:HttpRequest, *args, **kwargs):
    brands_with_count = Brand.objects.annotate(count=Count('products_brand'))
    categories_with_count = ProductCategory.objects.annotate(count=Count('categories'))
    
    order_query_by_price = Product.objects.order_by('price')
    min_price = 0
    max_price = order_query_by_price.last().price or 900000000
    start_price = request.GET.get('start_price') or min_price
    end_price = request.GET.get('end_price') or max_price
    
    banners = AdvertisingBanner.objects.filter(location__iexact="products-list-page")
    
    return render(request=request, template_name="includes/left-sidebar.html", context={
        'brands': brands_with_count,
        'list_category': categories_with_count,
        'start_price': start_price,
        'end_price': end_price,
        'max_price': max_price,
        'step': 1000000,
        'banners': banners,
    })