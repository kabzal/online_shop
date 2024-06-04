from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


@login_required
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return render(request,
                          template_name='orders/order/created.html',
                          context={'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  template_name='orders/order/create.html',
                  context={'cart': cart,
                           'form': form})

