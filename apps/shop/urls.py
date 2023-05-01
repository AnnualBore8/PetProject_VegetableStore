from django.urls import path
from .views import ShopView, ProductView

app_name = "shop"

urlpatterns = [
   path('', ShopView.as_view(), name="shop"),
   path('product/<int:product_id>', ProductView.as_view(), name="product-single"),
   path('product/', ProductView.as_view(), name="product-single"),
]
