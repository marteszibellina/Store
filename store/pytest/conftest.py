"""Pytest configuration."""

import pytest

from django.contrib.auth.models import User

from stock.models import Category, Product, ShoppingCart, SubCategory

@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(username='testuser',
                                    password='testpass')


@pytest.mark.django_db
def test_category_creation(db):
    """Test category creation."""
    category = Category.objects.create(name='Test Category',
                                       slug='test-category')
    assert category.name == 'Test Category'
    assert category.slug == 'test-category'

@pytest.mark.django_db
def test_subcategory_creation(db):
    """Test subcategory creation."""
    subcategory = SubCategory.objects.create(name='Test Subcategory',
                                             slug='test-subcategory',
                                             category='Test Category')

    assert subcategory.name == 'Test Subcategory'
    assert subcategory.slug == 'test-subcategory'
    assert subcategory.category == 'Test Category'


@pytest.fixture
def product(db):
    """Create a test product with related category and subcategory."""
    category = Category.objects.create(name='Test Category',
                                       slug='test-category')

    subcategory = SubCategory.objects.create(name='Test Subcategory',
                                             slug='test-subcategory',
                                             category=category)

    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        price='100.00',
        subcategory=subcategory
    )

@pytest.fixture
def shopping_cart(db, user, product):
    """Create a test shopping cart."""
    return ShoppingCart.objects.create(user=user,
                                       product=product,
                                       quantity=1)
