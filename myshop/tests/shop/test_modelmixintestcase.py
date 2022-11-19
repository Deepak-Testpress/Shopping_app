from django.test import TestCase
from shop.models import Product, Category


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            name="Gaming",
            slug="gaming",
        )

        self.product1 = Product.objects.create(
            category=self.category1,
            name="Play station 5",
            slug="play-station-5",
            description="A gaming console",
            price=50000.00,
        )
