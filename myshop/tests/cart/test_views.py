from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Category


class TestViews(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Gaming",
            slug="gaming",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Play station 5",
            slug="play-station-5",
            description="A gaming console",
            price=50000.00,
        )

    def test_cart_add_redirects_to_cart_detail(self):
        cart_add_url = reverse("cart:cart_add", kwargs={"product_id": "1"})
        cart_detail_url = reverse("cart:cart_detail")
        response = self.client.post(cart_add_url)

        self.assertEqual(cart_detail_url, response.url)

    def test_cart_remove_redirects_to_cart_detail(self):
        cart_remove_url = reverse("cart:cart_add", kwargs={"product_id": "1"})
        cart_detail_url = reverse("cart:cart_detail")
        response = self.client.post(cart_remove_url)

        self.assertEqual(cart_detail_url, response.url)

    def test_templates_used_for_cart_detail_view(self):
        cart_detail_url = reverse("cart:cart_detail")
        response = self.client.get(cart_detail_url)

        self.assertTemplateUsed(response, "cart/detail.html")

    def test_cart_add_returns_404_for_invalid_product(self):
        response = self.client.post(reverse("cart:cart_add", args=["2191"]))

        self.assertEquals(response.status_code, 404)

    def test_cart_remove_returns_404_for_invalid_product(self):
        response = self.client.post(reverse("cart:cart_remove", args=["2191"]))

        self.assertEquals(response.status_code, 404)
