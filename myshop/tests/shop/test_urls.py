from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import product_list, product_detail
from tests.shop.test_model_mixin_testcase import ModelMixinTestCase


class TestURLs(ModelMixinTestCase, SimpleTestCase):
    def test_product_list(self):
        product_list_url = reverse("shop:product_list")
        self.assertEqual((resolve(product_list_url).func), product_list)

    def test_product_list_by_category(self):
        product_list_by_category_url = reverse(
            "shop:product_list_by_category", args=[self.category1.slug]
        )
        self.assertEqual(
            (resolve(product_list_by_category_url).func), product_list
        )

    def test_product_detail(self):
        product_detail_url = reverse(
            "shop:product_detail",
            args=[self.product1.id, self.product1.slug],
        )
        self.assertEqual((resolve(product_detail_url).func), product_detail)
