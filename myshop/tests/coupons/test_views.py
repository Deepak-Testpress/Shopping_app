from django.test import TestCase
from django.urls import reverse
from tests.coupons.test_model_mixin_testcase import ModelMixinTestCase
from coupons.views import coupon_apply


class TestViews(ModelMixinTestCase, TestCase):
    def test_coupon_apply_redirects_to_cart_detail(self):
        response = self.client.post(reverse("coupons:apply"))

        self.assertEqual(response.url, "/cart/")

    def test_coupon_id_added_in_session_for_valid_coupon(self):
        request = self.get_request(
            method="POST", data={"code": self.valid_coupon_for_10_percent.code}
        )
        coupon_apply(request)

        self.assertEqual(
            self.valid_coupon_for_10_percent.id,
            request.session.get("coupon_id"),
        )

    def test_coupon_id_added_as_none_in_session_for_expired_coupon(self):
        request = self.get_request(
            method="POST",
            data={"code": self.expired_coupon_for_50_percent.code},
        )
        coupon_apply(request)

        self.assertIsNone(request.session.get("coupon_id"))

    def test_coupon_id_added_as_none_in_session_for_inactive_coupon(self):
        request = self.get_request(
            method="POST",
            data={"code": self.inactive_coupon_for_30_percent.code},
        )
        coupon_apply(request)

        self.assertIsNone(request.session.get("coupon_id"))

    def test_coupon_id_added_as_none_in_session_for_empty_coupon_code(self):
        request = self.get_request(
            method="POST",
            data={"code": self.inactive_coupon_for_30_percent.code},
        )
        coupon_apply(request)

        self.assertIsNone(request.session.get("coupon_id"))
