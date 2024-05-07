from django.urls import path
from . import views

app_name = "home_module"
urlpatterns = [
    path('', views.HomePageView.as_view(), name="home-page"),
    path('home-page/favorite-product/', views.FavoriteProductView.as_view(), name="favorite_product_page"),
    path('home-page/favorite-product/<int:product_id>/<int:user_id>/<str:method>/', views.FavoriteProductView.as_view(), name="favorite_product_page"),
    # path('home-page/delete-favorite-product/<int:product_id><str:method>', views.FavoriteProductView.as_view(), name="delete_favorite_product_page"),
    # path('', views.index_page, name="home_page"),
    # path('header-loader', views.header_loader_view, name="header_loader"),
    # path('footer-loader', views.footer_loader_view, name="footer_loader"),
]
