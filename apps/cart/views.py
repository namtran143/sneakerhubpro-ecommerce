from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.products.models import Product

from .cart import UserCart
from .models import CartItem

@login_required
def cart_detail_view(request):
    cart = UserCart(request.user)
    items = cart.items()
    return render(request, 'cart/detail.html', {
        'items': items,
        'cart_total': cart.subtotal(),
    })

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not product.in_stock:
        messages.warning(request, 'Sản phẩm hiện đang hết hàng.')
        return redirect(product.get_absolute_url())

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1},
    )
    if not created:
        item.quantity += 1
        item.save(update_fields=['quantity'])

    messages.success(request, f'Đã thêm "{product.name}" vào giỏ hàng.')
    return redirect(request.POST.get('next') or 'cart:detail')

@login_required
def update_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = max(1, int(request.POST.get('quantity', 1)))
    if quantity > item.product.stock:
        messages.warning(request, 'Số lượng vượt quá tồn kho hiện tại.')
        return redirect('cart:detail')
    item.quantity = quantity
    item.save(update_fields=['quantity'])
    messages.success(request, 'Đã cập nhật giỏ hàng.')
    return redirect('cart:detail')

@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('cart:detail')
