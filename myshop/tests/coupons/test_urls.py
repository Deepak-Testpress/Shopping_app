from django.test import SimpleTestCase
from django.urls import reverse, resolve
from coupons.views import coupon_apply


class TestURLs(SimpleTestCase):
    def test_coupon_apply(self):
        coupon_apply_url = reverse("coupons:apply")
        self.assertEqual((resolve(coupon_apply_url).func), coupon_apply)
