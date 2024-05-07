from django.urls import path
from . import views

app_name = "payment_module"
urlpatterns = [
    path('request/<int:order_id>/', views.send_request, name='payment_request'),
    path('verify/', views.verify , name='payment_verify'),
]
