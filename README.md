# SneakerHub - Django Ecommerce Marketplace

Project demo web thương mại điện tử chạy localhost bằng Django + SQLite, giao diện tiếng Việt theo phong cách sàn TMĐT lớn.

## Công nghệ
- Django 5.2.x
- SQLite
- Bootstrap 5
- Bootstrap Icons
- SwiperJS
- AOS
- Django media upload
- Auth built-in + custom user

## 1) Tạo môi trường ảo
```bash
py -3.14 -m venv .venv
.venv\Scripts\activate
```

## 2) Cài thư viện
```bash
pip install -r requirements.txt
```

## 3) Chạy migrate
```bash
python manage.py makemigrations users products cart orders
python manage.py migrate
```

## 4) Tạo tài khoản admin
```bash
python manage.py createsuperuser
```

## 5) Tạo dữ liệu demo
```bash
python manage.py seed_demo
```

## 6) Chạy server
```bash
python manage.py runserver
```

Truy cập:
- Trang chủ: http://127.0.0.1:8000/
- Auth: http://127.0.0.1:8000/auth/
- Admin: http://127.0.0.1:8000/admin/

## Tài khoản demo sau khi seed
- Seller: `sellerdemo` / `seller12345`

## Ghi chú
- QR Banking trong project là **QR demo nội bộ** để chạy localhost, không tích hợp cổng thanh toán thật.
- Ảnh sản phẩm có thể upload từ Django admin hoặc từ trang seller.
- Sau logout hệ thống chuyển về giao diện auth.
