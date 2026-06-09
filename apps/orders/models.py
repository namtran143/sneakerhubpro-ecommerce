from django.conf import settings
from django.db import models

from apps.products.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Chờ xử lý'
        PAID = 'paid', 'Đã thanh toán'
        SHIPPING = 'shipping', 'Đang giao'
        COMPLETED = 'completed', 'Hoàn tất'
        CANCEL = 'cancel', 'Đã hủy'

    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'Thanh toán khi nhận hàng'
        QR = 'QR', 'Chuyển khoản QR Banking'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    qr_code = models.ImageField(upload_to='qr/', blank=True, null=True)
    transfer_code = models.CharField(max_length=64, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def code(self):
        return f'DH{self.id:06d}' if self.id else 'DHXXXXXX'

    def __str__(self):
        return self.code

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.order.code} - {self.product.name}'
