from django import template

register = template.Library()

# @register.filter(name="dwc")
def digit_with_comma(value):
    return "{:,}".format(value) + " تومان"

register.filter(name='dwc', filter_func=digit_with_comma)
