from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.models import CartItem
from apps.products.models import Product

from .forms import CheckoutForm
from .models import Order, OrderItem
from .payment import generate_qr_svg, generate_transfer_code

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    if not cart_items.exists():
        messages.warning(request, 'Giỏ hàng đang trống.')
        return redirect('products:home')

    cart_total = sum(item.subtotal for item in cart_items)
    form = CheckoutForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total=cart_total,
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                payment_method=form.cleaned_data['payment_method'],
                note=form.cleaned_data['note'],
                status=Order.Status.PENDING,
            )

            for item in cart_items:
                product = item.product
                if item.quantity > product.stock:
                    messages.error(request, f'Sản phẩm "{product.name}" không đủ tồn kho.')
                    order.delete()
                    return redirect('cart:detail')

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.final_price,
                )
                product.stock -= item.quantity
                product.sold_count += item.quantity
                product.save(update_fields=['stock', 'sold_count'])

            if order.payment_method == Order.PaymentMethod.QR:
                order.transfer_code = generate_transfer_code(order)
                qr_relative_path = generate_qr_svg(order)
                order.qr_code = qr_relative_path
                order.save(update_fields=['transfer_code', 'qr_code'])
            else:
                order.save(update_fields=['status'])

            cart_items.delete()

        if order.payment_method == Order.PaymentMethod.QR:
            return redirect('orders:payment', order_id=order.id)
        messages.success(request, 'Đặt hàng COD thành công.')
        return redirect('orders:payment_success', order_id=order.id)

    return render(request, 'order/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
    })

@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.status = Order.Status.PAID
        order.save(update_fields=['status'])
        messages.success(request, 'Thanh toán QR thành công.')
        return redirect('orders:payment_success', order_id=order.id)
    return render(request, 'order/payment.html', {'order': order})

@login_required
def payment_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/payment_success.html', {'order': order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'order/history.html', {'orders': orders})
