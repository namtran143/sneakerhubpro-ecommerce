from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from apps.orders.models import Order
from apps.products.models import Product

from .forms import SellerProductForm

def seller_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:auth')
        if not request.user.is_seller and not request.user.is_superuser:
            return HttpResponseForbidden('Bạn không có quyền truy cập khu vực người bán.')
        return view_func(request, *args, **kwargs)
    return wrapped

@login_required
@seller_required
def dashboard_view(request):
    products = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(items__product__seller=request.user).distinct()
    total_revenue = orders.filter(status__in=[Order.Status.PAID, Order.Status.SHIPPING, Order.Status.COMPLETED]).aggregate(
        total=Sum('total')
    )['total'] or 0
    recent_orders = orders[:6]
    return render(request, 'seller/dashboard.html', {
        'product_count': products.count(),
        'order_count': orders.count(),
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    })

@login_required
@seller_required
def product_manage_view(request):
    products = Product.objects.filter(seller=request.user).select_related('category')
    return render(request, 'seller/product_manage.html', {'products': products})

@login_required
@seller_required
def product_create_view(request):
    form = SellerProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        messages.success(request, 'Đã tạo sản phẩm mới.')
        return redirect('seller:products')
    return render(request, 'seller/product_form.html', {'form': form, 'title': 'Thêm sản phẩm'})

@login_required
@seller_required
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = SellerProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Đã cập nhật sản phẩm.')
        return redirect('seller:products')
    return render(request, 'seller/product_form.html', {'form': form, 'title': 'Cập nhật sản phẩm'})

@login_required
@seller_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.info(request, 'Đã xóa sản phẩm.')
        return redirect('seller:products')
    return render(request, 'seller/product_delete.html', {'product': product})

@login_required
@seller_required
def order_manage_view(request):
    orders = Order.objects.filter(items__product__seller=request.user).distinct().prefetch_related('items__product')
    return render(request, 'seller/order_manage.html', {'orders': orders})
