from shop.models import Product, Category
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from datetime import timedelta
from coupons.models import Coupon


class ModelMixinTestCase(TestCase):
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

        self.valid_coupon_for_10_percent = Coupon.objects.create(
            code="FUNTEN",
            valid_from=timezone.now() - timedelta(30),
            valid_to=timezone.now() + timedelta(30),
            discount=10,
            active=True,
        )
        self.inactive_coupon_for_30_percent = Coupon.objects.create(
            code="30%OFF",
            valid_from=timezone.now() - timedelta(30),
            valid_to=timezone.now() + timedelta(30),
            discount=30,
            active=False,
        )
        self.expired_coupon_for_50_percent = Coupon.objects.create(
            code="GREAT50",
            valid_from=timezone.now() - timedelta(30),
            valid_to=timezone.now() - timedelta(20),
            discount=50,
            active=True,
        )

    def get_request(self, method, data):
        request = RequestFactory().get("/")
        middleware = SessionMiddleware(get_response=request)
        middleware.process_request(request)
        request.session.save()
        request.method = method
        request.POST = data

        return request
