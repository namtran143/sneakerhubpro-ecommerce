from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.products.models import Category, Product
from apps.users.models import User

class Command(BaseCommand):
    help = 'Tạo dữ liệu demo cho SneakerHub.'

    def handle(self, *args, **options):
        seller, _ = User.objects.get_or_create(
            username='sellerdemo',
            defaults={
                'email': 'seller@example.com',
                'display_name': 'SneakerHub Official',
                'role': User.Role.SELLER,
            }
        )
        if not seller.check_password('seller12345'):
            seller.set_password('seller12345')
            seller.save()

        categories = [
            ('Sneaker Nam', 'bi-lightning-charge'),
            ('Sneaker Nữ', 'bi-stars'),
            ('Chạy bộ', 'bi-bicycle'),
            ('Lifestyle', 'bi-bag-heart'),
            ('Phụ kiện', 'bi-gem'),
            ('Giảm sốc', 'bi-fire'),
        ]
        for name, icon in categories:
            Category.objects.get_or_create(name=name, slug=slugify(name), defaults={'icon': icon})

        sample_products = [
            ('Nike Air Zoom Pro', 2490000, 15, 'Mẫu giày chạy bộ linh hoạt, nhẹ và êm chân.', True, True),
            ('Adidas Street Move', 1890000, 10, 'Phong cách trẻ trung, phối đồ cực dễ.', True, False),
            ('Puma Velocity 2', 1590000, 25, 'Tối ưu cho tập luyện hằng ngày.', False, True),
            ('New Balance Urban Step', 2290000, 5, 'Thiết kế premium, hợp đi làm và đi chơi.', True, False),
            ('Asics Gel Max', 2790000, 20, 'Đệm tốt, phù hợp chạy dài.', False, False),
            ('Sneaker Care Kit', 199000, 0, 'Bộ vệ sinh giày mini tiện lợi.', False, False),
        ]
        category_list = list(Category.objects.all())
        for idx, (name, price, discount, desc, featured, flash) in enumerate(sample_products, start=1):
            Product.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    'category': category_list[(idx - 1) % len(category_list)],
                    'seller': seller,
                    'name': name,
                    'price': Decimal(price),
                    'discount_percent': discount,
                    'description': desc,
                    'stock': 50,
                    'sold_count': idx * 15,
                    'is_featured': featured,
                    'is_flash_sale': flash,
                }
            )

        self.stdout.write(self.style.SUCCESS('Đã tạo dữ liệu demo.'))
        self.stdout.write('Seller demo: sellerdemo / seller12345')
