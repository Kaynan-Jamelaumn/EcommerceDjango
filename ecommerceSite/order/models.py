from django.db import models

from ecommerceSite.product.models import ProductVariation

from ecommerceSite.account.models import Address
from django.conf import settings  # Here


# Create your models here.
class Order(models.Model):

    variation = models.ForeignKey(ProductVariation,
                                  on_delete=models.DO_NOTHING,
                                  related_name='orders')
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    total = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='order_user')

    def unity_price(self):
        return self.total / self.quantity


class Orders(models.Model):
    STATUS_CHOICES = (('C', 'CREATED'),
                      ('P', 'PAID_TO_DELIEVER'), ('D', 'DELIVERED'))

    order = models.ManyToManyField(Order)
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='orders_user')

    address = models.ForeignKey(Address,
                                on_delete=models.DO_NOTHING,
                                blank=False,
                                null=False)
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    total_paid = models.FloatField()


"""
class Orders(models.Model):
    STATUS_CHOICES = (('C', 'CREATED'),
                      ('P', 'PAID_TO_DELIEVER'), ('D', 'DELIVERED'))

    orders = models.ManyToManyField(Order, related_name='orders')
    created_at = models.DateField(auto_now_add=True)
    uploaded_at = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    address = models.ForeignKey(Address,
                                on_delete=models.DO_NOTHING,
                                blank=False,
                                null=False)
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    total_paid = models.FloatField()

"""
