# SneakerHubPro - Django E-commerce Website

SneakerHubPro is a demo e-commerce website for selling sneakers, built with Django, SQLite and Bootstrap 5.
The project focuses on core online shopping features such as product browsing, cart management, checkout, order history and seller product management.

## Features

### Customer

* Register, log in and manage user profile.
* Browse sneaker products by category.
* Search, filter and sort products.
* View product details and product reviews.
* Add products to cart, update quantity and remove items.
* Place orders using Cash on Delivery or QR demo payment.
* View order history.

### Seller

* Access seller dashboard.
* Create, update and delete products.
* View basic product and order information related to the seller's products.

### Admin

* Manage users, categories, products, reviews, carts and orders through Django Admin.

## Technologies

* Python
* Django 5.2.x
* SQLite
* HTML, CSS, Bootstrap 5
* Bootstrap Icons
* SwiperJS
* AOS
* Django Authentication
* Django Media Upload

## Project Structure

```text
sneakerhubpro/
├── apps/
│   ├── users/
│   ├── products/
│   ├── cart/
│   ├── orders/
│   └── seller/
├── sneakerhub/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/namtran143/sneakerhubpro-ecommerce.git
cd sneakerhubpro-ecommerce
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py makemigrations users products cart orders
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Seed demo data

```bash
python manage.py seed_demo
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Demo Account

After running the seed command, a demo seller account is available:

```text
Username: sellerdemo
Password: seller12345
```

## Notes

* This project is built for academic and portfolio purposes.
* The QR payment feature is a local demo only and is not integrated with a real payment gateway.
* Product images can be uploaded through Django Admin or the seller product management page.
* SQLite is used for local development and demonstration.
