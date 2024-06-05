from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # access the request session
    # it tries to get this variable if it exists and initalizes it to an empty dictionary if it doesn't
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            # if item already in bag, check if another item of same id and size exists
            # if so, increment quantity for that size
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # otherise set it to quantity
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # if item not already in bag, add it
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
    # create dictionary and add items
    #if it already exists, increase quantity
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # put bag variable into session
    request.session['bag'] = bag

    return redirect(redirect_url)