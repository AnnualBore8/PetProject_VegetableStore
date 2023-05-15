from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Product
from django.db.models import F, OuterRef, Subquery, DecimalField, ExpressionWrapper, Sum, Case, When
from django.utils import timezone


def fill_card_in_session(request):
    cart = request.session.get('cart', {})
    if not cart:
        cart_items = Cart.objects.filter(cart__user=request.user)
        for item in cart_items:
            cart[item.product.id] = item.quantity
        request.session['cart'] = cart
    return cart


class ViewCart(View):

    def get(self, request):
        # cart = fill_card_in_session(request)  # Пробуем получить корзину товаров из сессии
        # if cart:
        #     products = Product.objects.filter(id__in=cart.keys())
        #     data = [{"product": product, "quantity": cart[str(product.id)], 'id': product.id} for product in products]
        # else:
        #     data = []

        user_cart = Cart.objects.filter(user=request.user).select_related('product')
        total_discount = Case(When(product__discount__value__gte=0,
                                   product__discount__date_begin__lte=timezone.now(),
                                   product__discount__date_end__gte=timezone.now(),
                                   then=F('total_price') * F('product__discount__value') / 100),
                              default=0,
                              output_field=DecimalField(max_digits=10, decimal_places=2)
                              )
        cart = user_cart.annotate(
            total_price=F('product__price') * F('quantity'),
            total_discount=total_discount,
            total_price_with_discount=F('total_price') - F('total_discount'),
        )

        sum_data = cart.aggregate(sum_price=Sum('total_price'),
                                  sum_discount=Sum('total_discount'),
                                  sum_price_with_discount=Sum('total_price_with_discount'))

        context = {"data": cart}
        context.update(sum_data)

        return render(request, 'cart/cart.html', context)


class ViewWishlist(View):
    def get(self, request):
        return render(request, 'cart/wishlist.html')


class ViewCartDel(View):
    def get(self, request, product_id):
        cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        cart_item.delete()
        return redirect('cart:cart')
