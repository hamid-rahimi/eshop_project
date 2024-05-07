from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import F

from product_module.models import Product
from .models import Order, OrderItem


def get_order_detail(order: Order):
    if order:
        count_of_items = order.orderitem_set.all().count()
        total_order_price = sum(item.total_price() for item in order.orderitem_set.all())
        tax = total_order_price * 0.09
        total_sum = total_order_price + tax
        return count_of_items, total_order_price, tax, total_sum

@method_decorator(decorator=login_required, name='dispatch')
class AddToOrderView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        product_id = request.GET.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse(data={
                "title": "Not Found",
                "status": "error",
                "message": "کالای مورد نظر یافت نشد",
                "button": "بله متوجه شدم"
            })
        count = int(request.GET.get('count'))
        if count < 1 or count > product.count:
            return JsonResponse(data={
                "title": "Value Error",
                "status": "error",
                "message": "تعداد وارد شده نامعتبر است",
                "button": "بله متوجه شدم"
            })
        order, created = Order.objects.get_or_create(
            user=request.user, is_paid=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product,
                                                              defaults={'count': 0})
        total = order_item.count + count
        if total > product.count:
            return JsonResponse(data={
                "title": "Value Error",
                "status": "error",
                "message": "تعداد وارد شده بیش از حد مجاز است",
                "button": "بله متوجه شدم"
            })
        order_item.count = total
        order_item.save()
        return JsonResponse(data={
            "title": "Added",
            "status": "success",
            "message": "کالای مورد نظر با موفقیت به سبد خرید اضافه شد",
            "button": "بله متوجه شدم"
        })

@method_decorator(decorator=login_required, name='dispatch')
class OrderItemView(View):
    
    def get(self, request: HttpRequest, *args, **kwargs):
        order: Order = Order.objects.prefetch_related('orderitem_set').filter(
                        user=request.user, is_paid=False).first()
        if order:
            count_of_items, total_order_price, tax, total_sum = get_order_detail(order)
            return render(request, "order_module/order_item.html", {
                'order': order,
                'count_of_items': count_of_items,
                'total_order_price': total_order_price,
                'tax': tax,
                'total_sum': total_sum,
            })
        else:
            return render(request, "order_module/order_item.html", {
                'order': None,
            })
    
    # def increase_count(self, request: HttpRequest, *args, **kwargs):
    #     print(request.method)
    #     order_item: OrderItem = OrderItem.objects.filter(id=request.GET.get('order_item_id')).first()
    
    # def decrease_count(self, request: HttpRequest, *args, **kwargs):
    #     pass


class OrderItemDeleteView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        order_item_id = request.GET.get('order_item_id')
        order_item: OrderItem = OrderItem.objects.filter(id=order_item_id, payment_amount_for_once=0).first()
        order=order_item.order
        del_int, del_dict = order_item.delete()
        count_of_items, total_order_price, tax, total_sum = get_order_detail(order)
        if del_int == 1:
            return render(request, "order_module/includes/order_item_table.html", {
                'order': order,
                'count_of_items': count_of_items,
                'total_order_price': total_order_price,
                'tax': tax,
                'total_sum': total_sum,
            })
        else:
            return JsonResponse(data={
                "title": "خطا",
                "status": "error",
                "message": "خطا در حذف کالای مورد نظر.",
                "button": "بله متوجه شدم"
            })
        print(request.GET)


class OrderItemCountView(View):
    
    def get(self, request: HttpRequest, *args, **kwargs):
        order_item_id: int = request.GET.get('order_item_id')
        action: str = request.GET.get('action')
        order_item: OrderItem = get_object_or_404(OrderItem.objects.select_related('product'), id=order_item_id)
        if action == 'increase':
            if order_item.count + 1 > order_item.product.count:
                return JsonResponse(data={
                    "title": "Value Error",
                    "status": "error",
                    "message": "تعداد وارد شده بیش از حد مجاز است",
                    "button": "بله متوجه شدم"
                })
            else:
                OrderItem.objects.filter(id=order_item_id).update(count=F('count') + 1)
        elif action == 'decrease':
            if order_item.count - 1 < 1:
                return JsonResponse(data={
                    "title": "Value Error",
                    "status": "error",
                    "message": "تعداد وارد شده نامعتبر است",
                    "button": "بله متوجه شدم"
                })
            else:
                OrderItem.objects.filter(id=order_item_id).update(count=F('count') - 1)
        else:
            return JsonResponse(data={
                "title": "Value Error",
                "status": "error",
                "message": "عملیات وارد شده نامعتبر است",
                "button": "بله متوجه شدم"
            })
        order_item.refresh_from_db()
        order = order_item.order
        count_of_items, total_order_price, tax, total_sum = get_order_detail(order)
        return render(request, "order_module/includes/order_item_table.html", {
            'order': order,
            'count_of_items': count_of_items,
            'total_order_price': total_order_price,
            'tax': tax,
            'total_sum': total_sum,
        })
        