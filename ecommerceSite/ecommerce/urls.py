from django.urls import path, include
app_name = "ecommerce"
urlpatterns = [
    path('', include('ecommerceSite.product.urls', namespace='product')),
    path('account/', include('ecommerceSite.account.urls', namespace='account')),
    path('order/', include('ecommerceSite.order.urls', namespace='order')),
    path('cart/', include('ecommerceSite.cart.urls', namespace='cart')),
]
