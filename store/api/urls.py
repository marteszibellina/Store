"""API urls"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.views import (CategoryViewSet, get_subcategory_detail)
    #                     ProductImageViewSet,
    # ProductViewSet, ShoppingCartViewSet, SubCategoryViewSet)

router_default = DefaultRouter()

router_default.register('category', CategoryViewSet,
                        basename='category')
# router_default.register('subcategory', SubCategoryViewSet,
#                         basename='subcategory')
# router_default.register('product', ProductViewSet, basename='product')
# router_default.register('product_image', ProductImageViewSet,
#                         basename='product_image')
# router_default.register('cart', ShoppingCartViewSet, basename='cart')


urlpatterns = [
    path('', include(router_default.urls)),
    path('category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/',
         get_subcategory_detail),
]

router_simple = SimpleRouter()

# router_simple.register(
#     r'(?P<category_slug>\d+)/subcategory',
#     SubCategoryViewSet,
#     basename='subcategory',
# )
# # router_simple.register(
# #     r'(?P<category_slug>\d+)/(?P<subcategory_slug>\d+)/product',
# #     ProductViewSet,
# #     basename='product',
# # )
# # router_simple.register(
# #     r'(?P<category_slug>\d+)/(?P<subcategory_slug>\d+)/(?P<product_slug>\d+)/image',
# #     ProductImageViewSet,
# #     basename='product_image',
# # )

# urlpatterns = [
#     path('', include(router_default.urls)),
#     path('', include(router_simple.urls)),
# ]

# # Регистрация более сложных URL с параметрами
# # router_v1_simple.register(
# #     r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
# # )
# # router_v1_simple.register(
# #     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
# #     CommentViewSet,
# #     basename='comments',
# # )

# # urlpatterns = [
# #     # Подключение общего эндпоинта
# #     path('v1/', include([
# #         # Авторизация
# #         path('auth/token/', token_obtain_view),
# #         # Подключение роутера
# #         path('', include(router_v1.urls)),
# #         # Подключение роутера для сложных URL
# #         path('', include(router_v1_simple.urls)),
# #     ])),
# # ]