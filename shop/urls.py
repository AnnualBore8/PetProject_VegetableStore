from django.urls import path
from .views import ShopView, ProductView

app_name = "shop"

urlpatterns = [
   path('', ShopView.as_view(), name="shop"),
   path('product/', ProductView.as_view(), name="product-single"),
]
