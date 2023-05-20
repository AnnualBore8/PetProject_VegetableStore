from django.shortcuts import render
from django.views import View
from apps.cart.models import Product
from django.db.models import Case, When


class IndexShopView(View):

    def get(self, request):
        history = request.session.get("history", [])
        if history:
            ordering_conditions = [When(id=id_value, then=index) for
                                   index, id_value in enumerate(history)]
            data = Product.objects.filter(id__in=history).order_by(Case(*ordering_conditions))
        else:
            data = []
        context = {'data': data}

        # context = {'data': [{'name': 'Bell Pepper',
        #                      'discount': 30,
        #                      'price_before': 120.00,
        #                      'price_after': 80.00,
        #                      'url': 'store/images/product-1.jpg'},
        #                     {'name': 'Strawberry',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'url': 'store/images/product-2.jpg'},
        #                     {'name': 'Green Beans',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'url': 'store/images/product-3.jpg'},
        #                     {'name': 'Purple Cabbage',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'url': 'store/images/product-4.jpg'},
        #                     {'name': 'Tomatoe',
        #                      'discount': 30,
        #                      'price_before': 120.00,
        #                      'price_after': 80.00,
        #                      'url': 'store/images/product-5.jpg'},
        #                     {'name': 'Brocolli',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'url': 'store/images/product-6.jpg'},
        #                     {'name': 'Carrots',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'url': 'store/images/product-7.jpg'},
        #                     {'name': 'Fruit Juice',
        #                      'discount': None,
        #                      'price_before': 120.00,
        #                      'url': 'store/images/product-8.jpg'},
        #                     ]
        #            }

        return render(request, 'home/index.html', context)


class AboutView(View):

    def get(self, request):
        return render(request, 'home/about.html')


class ContactView(View):

    def get(self, request):
        return render(request, 'home/contact.html')
