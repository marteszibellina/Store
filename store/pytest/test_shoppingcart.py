import pytest

from rest_framework.reverse import reverse

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_shopping_cart_list(user, product):
    """Test GET shopping cart list."""
    client = APIClient()
    client.force_authenticate(user=user)  # forced, fix later

    response = client.get(reverse('shoppingcart-list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_shopping_cart(user, product):
    """Test POST shopping cart."""
    client = APIClient()
    client.force_authenticate(user=user)  # same

    data = {
        "product": product.id,
        "quantity": 2
    }

    response = client.post(reverse('shoppingcart-list'), data)

    assert response.status_code == 201
