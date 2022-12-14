from django.test import TestCase
from django.urls import reverse
from tests.coupons.test_model_mixin_testcase import ModelMixinTestCase
from coupons.views import coupon_apply


class TestViews(ModelMixinTestCase, TestCase):
    def test_coupon_apply_redirects_to_cart_detail(self):
        response = self.client.post(reverse("coupons:apply"))

        self.assertEqual(response.url, "/cart/")

    def test_coupon_id_added_in_session_for_valid_coupon(self):
        self.request.method = "POST"
        self.request.POST = {"code": self.valid_coupon_for_10_percent.code}
        coupon_apply(self.request)

        self.assertEqual(
            self.valid_coupon_for_10_percent.id,
            self.request.session.get("coupon_id"),
        )

    def test_coupon_id_added_as_none_in_session_for_expired_coupon(self):
        self.request.method = "POST"
        self.request.POST = {"code": self.expired_coupon_for_50_percent.code}
        coupon_apply(self.request)

        self.assertIsNone(self.request.session.get("coupon_id"))

    def test_coupon_id_added_as_none_in_session_for_inactive_coupon(self):
        self.request.method = "POST"
        self.request.POST = {"code": self.inactive_coupon_for_30_percent.code}
        coupon_apply(self.request)

        self.assertIsNone(self.request.session.get("coupon_id"))

    def test_coupon_id_added_as_none_in_session_for_empty_coupon_code(self):
        self.request.method = "POST"
        self.request.POST = {"code": ""}
        coupon_apply(self.request)

        self.assertIsNone(self.request.session.get("coupon_id"))

    def test_coupon_applies_discount_on_cart_total_price(self):
        self.request.method = "POST"
        self.request.POST = {"code": self.valid_coupon_for_10_percent.code}
        coupon_apply(self.request)

        quantity = 2
        self.cart.add_product(self.product, quantity=quantity)
        self.cart.coupon_id = self.request.session.get("coupon_id")

        total_price = self.product.price * quantity
        discount_price = total_price * (
            self.valid_coupon_for_10_percent.discount / 100
        )
        calucated_discount_price = total_price - discount_price

        self.assertEqual(
            calucated_discount_price,
            self.cart.get_total_price_after_discount(),
        )

    def test_coupon_doesnot_applies_discount_on_cart_total_price_if_expired(
        self,
    ):
        self.request.method = "POST"
        self.request.POST = {"code": self.expired_coupon_for_50_percent.code}
        coupon_apply(self.request)

        quantity = 2
        self.cart.add_product(self.product, quantity=quantity)
        self.cart.coupon_id = self.request.session.get("coupon_id")

        total_price = self.product.price * quantity
        discount_price = total_price * (
            self.expired_coupon_for_50_percent.discount / 100
        )
        calucated_discount_price = total_price - discount_price

        self.assertNotEqual(
            calucated_discount_price,
            self.cart.get_total_price_after_discount(),
        )

    def test_coupon_doesnot_applies_discount_on_cart_total_price_if_inactive(
        self,
    ):
        self.request.method = "POST"
        self.request.POST = {"code": self.inactive_coupon_for_30_percent.code}
        coupon_apply(self.request)

        quantity = 2
        self.cart.add_product(self.product, quantity=quantity)
        self.cart.coupon_id = self.request.session.get("coupon_id")

        total_price = self.product.price * quantity
        discount_price = total_price * (
            self.inactive_coupon_for_30_percent.discount / 100
        )
        calucated_discount_price = total_price - discount_price

        self.assertNotEqual(
            calucated_discount_price,
            self.cart.get_total_price_after_discount(),
        )
