from django import template

#register this filter
register = template.Library()

# use the register filter decorator to register function as a template filter.
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity