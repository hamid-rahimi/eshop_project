from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductView.as_view(), name="products-page"),
    path('product-by-category/<int:cat_id>/', views.ProductView.as_view(), name="products-page"),
    path('old/', views.ProductListView.as_view(), name="products-list-page"),
    path('favorite-product-list/', views.FavoriteProductListView.as_view(), name="favorite_product_list_page"),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name="product-detail"),
    # path('', views.products_view, name="products_page")
]
