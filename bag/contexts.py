from decimal import Decimal
from django.conf import settings 
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # iterate through all items in shopping bag 
    for item_id, item_data in bag.items():
        # only execute this is if item has no size
        # done by checking if it's an integer which shows quantity
        if isinstance(item_data, int):
            # get the product
            product = get_object_or_404(Product, pk=item_id)
            # add to the total cost
            total += item_data * product.price
            # add to the product count
            product_count += item_data
            #append items to bag
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            # otherwise we know it's a dictionary so iterate through items_by_size
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })  

    # calculate shipping costs
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        # let user know how much more money they need to spend to get free delivery
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total
    }
    
    return context