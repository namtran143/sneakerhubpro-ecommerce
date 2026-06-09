from decimal import Decimal

from .models import CartItem

class UserCart:
    def __init__(self, user):
        self.user = user

    def items(self):
        return CartItem.objects.filter(user=self.user).select_related('product')

    def count(self):
        return sum(item.quantity for item in self.items())

    def subtotal(self):
        total = Decimal('0.00')
        for item in self.items():
            total += item.subtotal
        return total
