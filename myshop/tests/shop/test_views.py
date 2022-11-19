from django.test import TestCase
from django.urls import reverse
from .test_modelmixintestcase import ModelMixinTestCase


class TestViews(ModelMixinTestCase, TestCase):
    def test_templates_used_for_product_list_view(self):
        self.product_list_url = reverse("shop:product_list")
        response = self.client.get(self.product_list_url)

        self.assertTemplateUsed(response, "shop/product/list.html")

    def test_templates_used_for_product_detail_view(self):
        self.product_list_url = reverse(
            "shop:product_detail",
            args=[self.product1.id, self.product1.slug],
        )
        response = self.client.get(self.product_list_url)

        self.assertTemplateUsed(response, "shop/product/detail.html")
