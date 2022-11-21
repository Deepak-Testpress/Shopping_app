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
        self.cart_add_url = reverse(
            "cart:cart_add", kwargs={"product_id": "1"}
        )
        self.cart_detail_url = reverse("cart:cart_detail")
        response = self.client.post(self.cart_add_url)

        self.assertEqual(self.cart_detail_url, response.url)

    def test_templates_used_for_cart_detail_view(self):
        self.cart_detail_url = reverse("cart:cart_detail")
        response = self.client.get(self.cart_detail_url)

        self.assertTemplateUsed(response, "cart/detail.html")
