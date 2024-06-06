from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.
def checkout(request):
    #get bag from session
    bag = request.session.get('bag', {})
    # if nothing in the bag, send error message
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    """ Create instance of order form """
    template = 'checkout/checkout.html'
    context = {
        'order form': order_form,
    }

    return render(request, template, context)