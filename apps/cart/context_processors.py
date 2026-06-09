from decimal import Decimal

from .cart import UserCart

def cart_summary(request):
    if request.user.is_authenticated:
        cart = UserCart(request.user)
        return {
            'cart_count': cart.count(),
            'cart_total': cart.subtotal(),
        }
    return {
        'cart_count': 0,
        'cart_total': Decimal('0.00'),
    }
