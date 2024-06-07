from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

# to execute the function any time the post_save signal is sent, use receiver
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    #instance.order refers to the order this specific line item is related to
    instance.order.update_total()

# update totals when item is deleted
@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    #instance.order refers to the order this specific line item is related to
    instance.order.update_total()