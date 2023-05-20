from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Product, Discount
from apps.cart.models import Cart
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.db.models.functions import Round, Cast
from decimal import Decimal
from apps.cart.views import fill_card_in_session


class ProductView(View):

    def get(self, request, product_id=1):
        history = request.session.get("history", [])
        if product_id not in history:
            if len(history) == 5:
                history.pop(0)
            history.append(product_id)
        else:
            history.remove(product_id)
            history.insert(0, product_id)
        request.session['history'] = history
        data = Product.objects.get(id=product_id)
        return render(request, 'shop/product-single.html', {"product": data})


def get_pages_list(page, max_pages):
    if max_pages < 5:
        return list(range(1, max_pages + 1))

    data = [1]
    if page > 3:
        data += ["..."]

    if 2 < page < max_pages - 1:
        data += list(range(page - 1, page + 2))
    elif page == 1:
        data += [2]
    elif page == 2:
        data += [2, 3]
    elif page == max_pages - 1:
        data += [page - 1, page]
    elif page == max_pages:
        data += [page - 1]

    if page + 2 < max_pages:
        data += ["..."]
    data += [max_pages]

    return data


class ShopView(View):

    def get(self, request):

        items_per_page = 5

        price_with_discount = ExpressionWrapper(
            F('price') * (100.0 - F('discount_value')) / 100.0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        products = Product.objects.select_related('category').annotate(
            discount_value=Subquery(
                Discount.objects.filter(product_id=OuterRef('id')).values('value')
            ),
            price_before=F('price'),
            price_after=price_with_discount,
        ).values('id', 'name', 'image', 'category', 'price_before', 'price_after', 'discount_value')

        category = request.GET.get("category", "All")
        if not category == "All":
            products = products.filter(category__name=category)

        paginator = Paginator(products, items_per_page)
        page = int(request.GET.get('page', 1))
        items = paginator.get_page(page)

        max_pages = paginator.num_pages
        data_pages = get_pages_list(page, max_pages)

        return render(request, 'shop/shop.html',
                      {"data": items,
                       "category": category,
                       "page": page,
                       "next": items.has_next(),
                       "previous": items.has_previous(),
                       "max_pages": max_pages,
                       "data_pages": data_pages})


def add_to_card_in_session(request, product_id):
    cart = fill_card_in_session(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return cart


class ViewCartBuy(View):
    def get(self, request, product_id):
        add_to_card_in_session(request, product_id)
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            user = get_object_or_404(User, id=request.user.id)
            cart_items = Cart.objects.filter(user=user, product=product)
            if cart_items:
                cart_item = cart_items[0]
                cart_item.quantity += 1
            else:
                cart_item = Cart(user=user, product=product)
            cart_item.save()
        return redirect('cart:cart')


class ViewCartAdd(View):
    def get(self, request, product_id):
        add_to_card_in_session(request, product_id)
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            user = get_object_or_404(User, id=request.user.id)
            cart_items = Cart.objects.filter(user=user, product=product)
            if cart_items:
                cart_item = cart_items[0]
                cart_item.quantity += 1
            else:
                cart_item = Cart(user=user, product=product)
            cart_item.save()
        data = "&".join([f"{key}={value}" for key, value in request.GET.items()])
        return redirect(reverse('shop:shop')+"?"+data)
