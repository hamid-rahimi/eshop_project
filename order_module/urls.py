from django.urls import path
from . import views

app_name = "order_module"
urlpatterns = [
    path('', views.AddToOrderView.as_view(), name='add_to_order_page'),
    path('order-item/', views.OrderItemView.as_view(), name='order_item_page'),
    path('order-item-delete/', views.OrderItemDeleteView.as_view(), name='order_item_delete_page'),
    path('order-item-count/', views.OrderItemCountView.as_view(), name='order_item_count_page'),
    # path('order-complete/<int:pk>/', OrderCompleteView.as_view(), name='order_complete_page'),
    # path('order-list/', OrderListView.as_view(), name='order_list_page'),
    # path('order-item-list/', OrderItemListView.as_view(), name='order_item_list_page'),
    # path('order-item-detail/<int:pk>/', OrderItemDetailView.as_view(), name='order_item_detail_page'),
    # path('order-item-cancel/<int:pk>/', OrderItemCancelView.as_view(), name='order_item_cancel_page'),
    # path('order-item-complete/<int:pk>/', OrderItemCompleteView.as_view(), name='order_item_complete_page'),
    # path('order-item-reject/<int:pk>/', OrderItemRejectView.as_view(), name='order_item_reject_page'),
]
