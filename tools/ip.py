def get_client_ip_address(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_address = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_address = req_headers.get('REMOTE_ADDR')
    return ip_address
    