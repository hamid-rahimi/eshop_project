from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.db.models import Count
from django.contrib.auth import get_user_model

from tools.group_list import convert_to_group_list
from product_module.models import Product, ProductCategory
from . import models



class HomePageView(TemplateView):

    template_name = "home_module/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = models.Slider.objects.filter(is_active=True)
        
        most_visited = list(Product.objects.filter(is_active=True, is_delete=False).
                            annotate(visited_count=Count("visited_product")).order_by('-visited_count')[:12])
        context['most_visited'] = convert_to_group_list(most_visited)
        
        newest_products = list(Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12])
        context['newest_products'] = convert_to_group_list(newest_products)
        
        groupe_categories = ProductCategory.objects.annotate(
                product_category_count=Count('product_categories')).filter(
                is_active=True,
                product_category_count__gt=0,
                categories__isnull=False)
        context['groupe_categories'] = groupe_categories
        
        return context

class FavoriteProductView(View):
    
    def dispatch(self, request:HttpRequest, *args, **kwargs):
        print(request.method)
        print(request.GET)
        method = request.GET.get('method')
        if (method is not None) and method == 'delete':
            request.method = method.upper()
        print(request.method)
        return super().dispatch(self.request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        print(kwargs)
        product_id = request.GET.get('product_id')
        user = get_user_model().objects.filter(id=request.user.id).first()
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            favorite_item = models.FavoriteProduct.objects.filter(product=product, user=user).first()
            del_count, del_dict = favorite_item.delete_item()
            return JsonResponse(data={
                'status': "success",
                'message': "حذف ایتم از لیست پسندشده"
            })
        return JsonResponse(data={
            'status': "error",
            'message': "خطا دز حذف ایتم مورد پسند"
        })
    
    def list(self, request, *args, **kwargs):
        user = get_user_model().objects.filter(id=request.user.id).first()
        favorite_products = models.FavoriteProduct.objects.filter(user=user)
        products_list = []
        for item in favorite_products:
            products_list.append(item.product)
        return JsonResponse(data={
            'products': products_list
        })
    
    def get(self, request, *args, **kwargs):

        favorite_product = Product.objects.filter(id=self.request.GET.get('product_id')).first()
        favorite_user = get_user_model().objects.filter(id=self.request.GET.get('user_id')).first()
        if (favorite_product is not None) and (favorite_user is not None):
            x, y = models.FavoriteProduct.objects.get_or_create(product=favorite_product, user=favorite_user)
            print(x,y)
        return render(request, "home_module/favorite_product.html")
    

            

def header_loader_view(request):
    favorite = models.FavoriteProduct.objects.all()
    return render(request, "shared/site_header_loader.html", {
        'favorite': favorite,
    })

def footer_loader_view(request):
    return render(request,"shared/site_footer_loader.html")

