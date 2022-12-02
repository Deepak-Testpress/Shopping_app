from django.test import TestCase
from django.urls import reverse
from tests.shop.test_model_mixin_testcase import ModelMixinTestCase
from shop.models import Product


class TestViews(ModelMixinTestCase, TestCase):
    def test_templates_used_for_product_list_view(self):
        product_list_url = reverse("shop:product_list")
        response = self.client.get(product_list_url)

        self.assertTemplateUsed(response, "shop/product/list.html")

    def test_templates_used_for_product_list_view_with_category_slug(self):
        product_list_by_category_url = reverse(
            "shop:product_list_by_category", args=[self.category1.slug]
        )
        response = self.client.get(product_list_by_category_url)

        self.assertTemplateUsed(response, "shop/product/list.html")

    def test_templates_used_for_product_detail_view(self):
        product_list_url = reverse(
            "shop:product_detail",
            args=[self.product1.id, self.product1.slug],
        )
        response = self.client.get(product_list_url)

        self.assertTemplateUsed(response, "shop/product/detail.html")

    def test_product_detail_returns_404_for_invalid_slug(self):
        product_detail_url = reverse(
            "shop:product_detail",
            args=[self.product1.id, "invalid_product_slug"],
        )
        response = self.client.get(product_detail_url)

        self.assertEquals(404, response.status_code)

    def test_post_list_shows_all_product_when_category_not_selected(self):
        products = Product.objects.all()
        request = self.client.get(reverse("shop:product_list"))
        self.assertQuerysetEqual(products, request.context.get("products"))

    def test_post_list_shows_category_based_products_when_category_is_selected(
        self,
    ):
        category_book = Product.objects.filter(category=self.category1)
        request = self.client.get(
            reverse("shop:product_list_by_category", args=["gaming"])
        )

        self.assertQuerysetEqual(
            category_book, request.context.get("products")
        )

    def test_post_list_shows_404_when_category_does_not_exists(self):
        response = self.client.get(
            reverse(
                "shop:product_list_by_category", args=["invalid_category_slug"]
            )
        )
        self.assertEquals(404, response.status_code)
