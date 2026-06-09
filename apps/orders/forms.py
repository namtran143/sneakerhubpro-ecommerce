from django import forms
from .models import Order

class CheckoutForm(forms.Form):
    address = forms.CharField(
        label='Địa chỉ nhận hàng',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố'})
    )
    phone = forms.CharField(
        label='Số điện thoại',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 098xxxxxxx'})
    )
    payment_method = forms.ChoiceField(
        label='Phương thức thanh toán',
        choices=Order.PaymentMethod.choices,
        widget=forms.RadioSelect
    )
    note = forms.CharField(
        label='Ghi chú',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ghi chú thêm cho người bán...'})
    )
