from django.db import models
from django.urls import reverse

# Create your models here.
class ContactUs(models.Model):
    title = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)
    fullname = models.CharField(max_length=300)
    message = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)
    response_time = models.DateTimeField(auto_now=True, blank=True)
    is_read_by_admin = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("accept_page", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return str(self.title)    
    class Meta:
        db_table = "contact"
        verbose_name = "تماس با ما"
        verbose_name_plural = "لیست تماس ها"
    
    