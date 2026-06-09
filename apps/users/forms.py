from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Tên đăng nhập',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập username'})
    )
    password = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'})
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    display_name = forms.CharField(
        label='Tên hiển thị',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Trang Store'})
    )
    role = forms.ChoiceField(
        label='Vai trò',
        choices=(
            (User.Role.CUSTOMER, 'Người mua'),
            (User.Role.SELLER, 'Người bán'),
        ),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password1 = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tạo mật khẩu'})
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'display_name', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email này đã được sử dụng.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.display_name = self.cleaned_data['display_name']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['display_name', 'email']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
