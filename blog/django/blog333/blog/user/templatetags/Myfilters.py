from django.template import Library

register = Library()

@register.filter('multiply')
def multiply(a,b):
    return int(a)*int(b)