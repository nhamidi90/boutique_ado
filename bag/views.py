from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # access the request session
    # it tries to get this variable if it exists and initalizes it to an empty dictionary if it doesn't
    bag = request.session.get('bag', {})

    # create dictionary and add items
    #if it already exists, increase quantity
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # put bag variable into session
    request.session['bag'] = bag

    return redirect(redirect_url)