"""VIEWSETS for API"""

from django.shortcuts import render


from django.contrib.auth import get_user_model
from django.db.models import F, Sum, FloatField, ExpressionWrapper
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from api.pagination import StandartPagination
from api.permissions import (IsAuthorOrReadOnly, IsReadOnly, IsAuthenticated)
from api.serializers import (CategorySerializer, ProductSerializer,
                            ProductImageSerializer,
                            ShoppingCartSerializer,
                            SubCategorySerializer)
from stock.models import (Category, Product,
                          ProductImage, ShoppingCart, SubCategory)

User = get_user_model()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandartPagination
    lookup_field = 'slug'

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[permissions.AllowAny],
        url_path='subcategory',
    )
    def get_subcategory(self, request, slug):
        """Subcategory viewset."""
        subcategory = SubCategory.objects.filter(category__slug=slug)
        serializer = SubCategorySerializer(subcategory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_subcategory_detail(self, category_slug, subcategory_slug):
    """Subcategory detail viewset."""

    try:
        subcategory = SubCategory.objects.get(
            slug=subcategory_slug,
            category__slug=category_slug,
        )
    except SubCategory.DoesNotExist:
        return Response({'detail': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = SubCategorySerializer(subcategory)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_product_detail(self, category_slug, subcategory_slug, product_slug):
    """Product detail viewset."""

    try:
        product = Product.objects.get(
            slug=product_slug,
            subcategory__slug=subcategory_slug,
            subcategory__category__slug=category_slug
        )
    except Product.DoesNotExist:
        return Response({'detail': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """ShoppingCart viewset."""

    serializer_class = ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandartPagination

    def get_queryset(self):
        """Get queryset for ShoppingCart viewset."""
        user = self.request.user
        return ShoppingCart.objects.filter(user=user)

    def perform_create(self, serializer):
        """Add product to cart."""
        user = self.request.user
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item, created = ShoppingCart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer.instance = cart_item

    def update(self, request, *args, **kwargs):
        """Edit quantity of product in cart."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        instance.quantity = serializer.validated_data.get('quantity',
                                                          instance.quantity)
        instance.save()
        return Response(self.get_serializer(instance).data)

    @action(detail=False, methods=['get'], url_path='summary')
    def cart_summary(self, request):
        """Get summary of cart."""
        cart_items = self.get_queryset()
        total_quantity = (cart_items.aggregate(total=Sum('quantity'))['total']
                          or 0)
        total_price = cart_items.annotate(
            item_total=ExpressionWrapper(F('quantity') * F('product__price'),
                                         output_field=FloatField())
        ).aggregate(sum=Sum('item_total'))['sum'] or 0

        serializer = self.get_serializer(cart_items, many=True)
        return Response({
            'items': serializer.data,
            'total_quantity': total_quantity,
            'total_price': round(total_price, 2)
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        """Clear cart."""
        self.get_queryset().delete()
        return Response({'message': 'Корзина очищена'},
                        status=status.HTTP_204_NO_CONTENT)
