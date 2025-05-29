"""Admin for the Stock"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from stock.models import (Category, Product,
                          ProductImage, ShoppingCart, SubCategory)

User = get_user_model()


class SubCategoryInline(admin.TabularInline):
    """SubCategory inline."""
    model = SubCategory
    fields = ('name', 'slug', 'image')
    extra = 1


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """SubCategory admin."""
    list_display = ('name', 'slug', 'image', 'category')
    search_fields = ('name', 'slug')
    list_display_links = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-empty-'


class ProductImageInline(admin.TabularInline):
    """ProductImage inline."""
    model = ProductImage
    fields = ('image', 'order')
    extra = 1


class ProductInline(admin.TabularInline):
    """Product inline."""
    model = Product
    fields = ('name', 'slug', 'get_category', 'subcategory', 'price',)
    readonly_fields = ('get_category',)
    extra = 1

    def get_category(self, obj):
        return obj.sub_category.category.name
    get_category.short_description = 'Category'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin."""
    list_display = ('name', 'slug', 'subcategory', 'price')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-empty-'
    inlines = (ProductImageInline, )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """ProductImage admin."""
    list_display = ('image', 'order', 'product')
    search_fields = ('image', 'order', 'product')
    empty_value_display = '-empty-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""
    list_display = ('name', 'slug', 'image',)
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-empty-'
    inlines = (SubCategoryInline,)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """ShoppingCart admin."""
    list_display = ('user', 'product', 'quantity',)
    search_fields = ('user', 'product', 'quantity',)
    empty_value_display = '-empty-'


admin.site.unregister(Group)
