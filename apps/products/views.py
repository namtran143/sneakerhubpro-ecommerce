from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Category, Product, Review

def home_view(request):
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.filter(is_featured=True)[:10]
    flash_sale_products = Product.objects.filter(is_flash_sale=True)[:10]
    new_products = Product.objects.all()[:15]
    return render(request, 'home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'flash_sale_products': flash_sale_products,
        'new_products': new_products,
    })

def product_list_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'new')

    products = Product.objects.select_related('seller', 'category').all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'sold':
        products = products.order_by('-sold_count')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'product/list.html', {
        'page_obj': page_obj,
        'query': query,
        'category_slug': category_slug,
        'sort': sort,
        'categories': Category.objects.all(),
    })

def product_detail_view(request, slug):
    product = get_object_or_404(Product.objects.select_related('seller', 'category'), slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:10]
    review_form = ReviewForm()
    return render(request, 'product/detail.html', {
        'product': product,
        'related_products': related_products,
        'review_form': review_form,
    })

@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        review, created = Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults=form.cleaned_data,
        )
        messages.success(
            request,
            'Đánh giá đã được gửi.' if created else 'Đánh giá của bạn đã được cập nhật.'
        )
    else:
        messages.error(request, 'Không thể gửi đánh giá. Vui lòng kiểm tra lại dữ liệu.')

    return redirect(product.get_absolute_url())
