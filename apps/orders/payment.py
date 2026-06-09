from pathlib import Path
import random

from django.conf import settings

BANK_NAME = 'MB Bank'
ACCOUNT_NO = '123456789'
ACCOUNT_NAME = 'SNEAKERHUB STORE'


def generate_transfer_code(order):
    return f'SH{order.id}{random.randint(1000, 9999)}'


def generate_qr_svg(order):
        return 'qr/srs.jpg'