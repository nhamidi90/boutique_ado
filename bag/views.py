from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
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
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]['items_by_size'][size]}')
            else:
                # otherise set it to quantity
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            # if item not already in bag, add it
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
    # create dictionary and add items
    #if it already exists, increase quantity
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    # put bag variable into session
    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            #if size drill into items by size dictionary, find size and set size to updated quantity
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]['items_by_size'][size]}')

        else:
            # or remove it if 0
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    # put bag variable into session
    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            # if size dictionary is empty, remove entire id so you don't end up with empty item by size dictionary
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        # put bag variable into session
        request.session['bag'] = bag
        
        # Because this view will be posted to from a JavaScript function you must 
        # return an actual 200 HTTP response
        return HttpResponse(status=200)
    
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)