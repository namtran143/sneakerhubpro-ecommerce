from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    icon = models.CharField(max_length=50, default='bi-grid')

    class Meta:
        ordering = ['name']
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(90)])
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_flash_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def final_price(self):
        if not self.discount_percent:
            return self.price
        discount = (Decimal(self.discount_percent) / Decimal('100')) * self.price
        return self.price - discount

    @property
    def average_rating(self):
        return round(self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0, 1)

    @property
    def total_reviews(self):
        return self.reviews.count()

    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product_review_per_user')
        ]

    def __str__(self):
        return f'{self.product.name} - {self.user}'
