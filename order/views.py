from django.shortcuts import render, redirect
from .models import Orders, Order

from product.models import ProductVariation
from account.models import Address
from cart.cart import Cart


# Create your views here.
def order_info(request, id):
    if not request.user.is_authenticated:
        return redirect('account:login')
    orders = Orders.objects.get(id=id, user=request.user)
    if orders is None:
        redirect('account:dashboard')
    return render(request, 'order/order_details.html', {'orders': orders})


def pay(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
      
    cart = Cart(request)
    if not cart.cart_total() > 0:
        return redirect('product:index')
      
    if request.method == 'GET':
        cart = Cart(request)
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'order/create.html', {
            'addresses': addresses,
            'total': cart.cart_total()
        })
    if request.method == 'POST':
        address = request.POST.get('address')
        if not address:
            return redirect('account:address-register')
          
        cart = Cart(request)
        productList = [ [], [], [], [] ] #ID Quantity price total
        address = Address.objects.get(id=address)
        orderList = []
      
        for key, value in cart.get_product().items():  #pega a quantidade total preço
            variationObject = ProductVariation.objects.get(
                id=int(key))
            if variationObject.stock < int(value.get('quantity')):
              return redirect('cart:view', )
              
            orderObject = Order(user=request.user, variation=variationObject, quantity=value.get('quantity'), total=float(value.get('totalitem')))
            orderObject.save()
            orderList.append(orderObject)
            ProductVariation.objects.filter(id=variationObject.id).update(stock=(variationObject.stock-float(value.get('totalitem'))))
        ordersObject = Orders.objects.create(user=request.user, address=address, total_paid=cart.cart_total(), status='P')
      
        for order in orderList:
            ordersObject.order.add(order)
      
        ordersObject.save()
        cart = cart.clear()
        return redirect('account:dashboard')
