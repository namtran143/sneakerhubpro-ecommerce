from django.conf import settings
from django.db import models

from apps.products.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_cart_item_per_user')
        ]

    @property
    def subtotal(self):
        return self.product.final_price * self.quantity

    def __str__(self):
        return f'{self.user} - {self.product}'
