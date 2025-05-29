"""API urls"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.views import (CategoryViewSet, get_subcategory_detail,
                       get_product_detail, ShoppingCartViewSet,)
    #                     ProductImageViewSet,
    # ProductViewSet, ShoppingCartViewSet, SubCategoryViewSet)

router_default = DefaultRouter()

router_default.register('category', CategoryViewSet,
                        basename='category')
router_default.register('shoppingcart', ShoppingCartViewSet,
                        basename='shoppingcart')

urlpatterns = [
    path('', include(router_default.urls)),
    path('category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/',
         get_subcategory_detail),
    path('category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/product/<slug:product_slug>/',
        get_product_detail
    ),
]
