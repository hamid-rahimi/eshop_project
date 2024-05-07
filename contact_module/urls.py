from django.urls import path
from . import views

app_name = "contact_module"
urlpatterns = [
    # path('', views.contact_us, name="contact_us_page"),
    # path('', views.ContactUsView.as_view(), name="contact_us_page"),
    path('', views.ContactUsFormView.as_view(), name="contact_us_page"),
    path('accept/<int:message_id>/', views.accepted_page, name="accepted-page"),
]
