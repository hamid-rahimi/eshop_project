from django.shortcuts import redirect, render
from eshop_project import settings
from django.http import HttpResponse, HttpRequest
import requests
import json
import datetime

from order_module.models import Order
from order_module.views import get_order_detail


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'

amount = 0  # Rial / Required
phone = '09124374986'  # Optional


def send_request(request: HttpRequest, order_id: int):
    order: Order = Order.objects.prefetch_related('orderitem_set').filter(id=order_id, user=request.user, is_paid=False).first()
    count_of_items, total_order_price, tax, total_sum = get_order_detail(order)
    description = f"برای {count_of_items} قلم کالا {total_order_price * 10} ریال بعلاوه {tax * 10} ریال مالیات پرداخت کنید."    
    data = {
        "MerchantID": settings.MERCHANT_ID,
        "Amount": total_sum * 10,
        "Description": description,
        "Phone": request.user.userprofile.mobile,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        print("1 ",response.status_code, response.json())
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                authority = response['Authority']
                return redirect(f"{ZP_API_STARTPAY}{authority}")
                # return HttpResponse(json.dumps({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': False, 'code': str(response['Status'])}), content_type='application/json')
        return HttpResponse(json.dumps(response), content_type='application/json')
        print("2 ",response.status_code, response)
    
    except requests.exceptions.Timeout:
        return HttpResponse(json.dumps({'status': False, 'code': 'timeout'}))
    except requests.exceptions.ConnectionError:
        return HttpResponse(json.dumps({'status': False, 'code': 'connection error'}))


def verify(request: HttpRequest):
    current_order: Order = Order.objects.filter(user=request.user, is_paid=False).first()
    tax = current_order.get_tax()
    total_price = current_order.calculate_total_price()
    
    print(request.GET, amount)
    data = {
        "MerchantID": settings.MERCHANT_ID,
        "Amount": (tax + total_price) *10,
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            current_order.is_paid = True
            current_order.payment_time = datetime.datetime.now()
            current_order.tax = tax
            current_order.reference_id = response['RefID']
            current_order.save()
            for order_item in current_order.orderitem_set.all():
                order_item.payment_amount_for_once = order_item.product.price
                order_item.save()
            return HttpResponse(f"Status : {response['Status']}, 'RefID': {response['RefID']}")
        else:
            return HttpResponse(f"Status : {response['Status']}, 'code': {str(response['Status'])}")
    return HttpResponse(json.dumps(response.json()), content_type='json/application')
