from django.shortcuts import render
from django.views import View
from .models import Product, Discount
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models.functions import Round, Cast
from decimal import Decimal

class ProductView(View):

    def get(self, request, product_id=1):
        data = Product.objects.get(id=product_id)
        return render(request, 'shop/product-single.html', {"product": data})


def get_pages_list(page, max_pages):
    if max_pages < 5:
        return list(range(1, max_pages + 1))
    data = [1]

    if page - 2 > 1:
        data = [1, "..."]

    if 2 < page < max_pages - 1:
        data += list(range(page - 1, page + 2))
    elif 2 < page:
        data += [page - 1, page]
    else:
        data += [page]

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
        page = request.GET.get('page', 1)
        items = paginator.get_page(page)

        max_pages = paginator.num_pages
        data_pages = [1, None, max_pages]







        return render(request, 'shop/shop.html',
                      {"data": items,
                       "category": category,
                       "page": page,
                       "next": items.has_next(),
                       "previous": items.has_previous(),
                       "max_pages": max_pages,
                       "data_pages": data_pages})
