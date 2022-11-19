from django.test import TestCase
from .test_modelmixintestcase import ModelMixinTestCase


class TestModelMethods(ModelMixinTestCase, TestCase):
    def test_category_gets_absolute_url(self):
        category_url = "/{category_slug}/".format(
            category_slug=self.category1.slug
        )
        self.assertEqual(category_url, self.category1.get_absolute_url())

    def test_product_gets_absolute_url(self):
        product_url = "/{product_id}/{product_slug}/".format(
            product_id=self.product1.id, product_slug=self.product1.slug
        )
        self.assertEqual(product_url, self.product1.get_absolute_url())
