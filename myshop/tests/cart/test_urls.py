from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart.views import cart_add, cart_detail


class TestURLs(SimpleTestCase):
    def test_cart_add(self):
        cart_add_url = reverse("cart:cart_add", kwargs={"product_id": "1"})
        self.assertEqual((resolve(cart_add_url).func), cart_add)

    def test_cart_detail(self):
        cart_detail_url = reverse("cart:cart_detail")
        self.assertEqual((resolve(cart_detail_url).func), cart_detail)
