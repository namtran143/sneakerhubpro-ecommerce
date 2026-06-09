from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Người mua'
        SELLER = 'seller', 'Người bán'
        ADMIN = 'admin', 'Quản trị viên'

    email = models.EmailField(unique=True)
    display_name = models.CharField('Tên hiển thị', max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    REQUIRED_FIELDS = ['email', 'display_name']

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role != self.Role.ADMIN:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name or self.username
