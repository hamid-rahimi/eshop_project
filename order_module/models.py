from django.db import models


class Order(models.Model):
    user = models.ForeignKey(to='account_module.User', on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده یا خیر')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت سفارش')
    payment_time = models.DateTimeField(blank=True, null=True, verbose_name='زمان پرداخت')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')
    tax = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='مالیات')
    transport = models.IntegerField(default=0, verbose_name='حمل و نقل')
    discount = models.DecimalField(default=0.0, max_digits=3, decimal_places=2,verbose_name='تخفیف')
    reference_id = models.CharField(max_length=64, null=True, blank=True, verbose_name='شماره پی گیری')

    def __str__(self):
        return str(self.user)
    
    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_item in self.orderitem_set.all():
                total_amount += order_item.payment_amount_for_once * order_item.count
        else:
            for order_item in self.orderitem_set.all():
                total_amount += order_item.product.price * order_item.count

        return total_amount
    
    def get_tax(self):
        return self.calculate_total_price() * 0.09
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey(to='product_module.Product', on_delete=models.CASCADE, verbose_name='محصول')
    payment_amount_for_once = models.IntegerField(default=0, verbose_name='مبلغ پرداختی هر محصول')
    count = models.IntegerField(default=1, verbose_name='تعداد')
    discount = models.DecimalField(default=0.0, max_digits=3, decimal_places=2,verbose_name='تخفیف')
    
    def __str__(self):
        return self.product.title
    
    def total_price(self):
        return self.product.price * self.count
    
    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'
    

