from django.shortcuts import render
from django.views import View
from .models import Product, Discount
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404
from django.db.models.functions import Round, Cast
from decimal import Decimal

class ProductView(View):

    def get(self, request, product_id=1):
        data = Product.objects.get(id=product_id)
        return render(request, 'shop/product-single.html', {"product": data})


class ShopView(View):

    def get(self, request):

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

        return render(request, 'shop/shop.html',
                      {"data": products,
                       "category": category})
