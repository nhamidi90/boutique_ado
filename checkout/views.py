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
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51POfMWFXybyjCv4JxkXCjikMFwTcSh3ly23WHeRLstrW4qJT0stjumrl8lbIpfUcGadl0D4689ETbJhXjYqcqvPl00vGL54FaY,'
    }

    return render(request, template, context)