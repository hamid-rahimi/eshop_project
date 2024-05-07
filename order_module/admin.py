from django.contrib import admin
from . import models


admin.site.site_header = 'مدیریت سایت فروشگاه'
admin.site.site_title = ' ادمین فروشگاه'
admin.site.index_title = 'پانل مدیریت سایت'

admin.site.register(models.Order)
admin.site.register(models.OrderItem)
