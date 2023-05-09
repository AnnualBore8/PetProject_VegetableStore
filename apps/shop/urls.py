from django.urls import path
from .views import ShopView, ProductView, ViewCartBuy, ViewCartAdd

app_name = "shop"

urlpatterns = [
   path('', ShopView.as_view(), name="shop"),
   path('product/<int:product_id>', ProductView.as_view(), name="product-single"),
   path('product/', ProductView.as_view(), name="product-single"),
   path('buy/<int:product_id>', ViewCartBuy.as_view(), name='buy'),
   path('add/<int:product_id>', ViewCartAdd.as_view(), name='add'),
]
