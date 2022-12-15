from django.test import TestCase, RequestFactory
from cart.cart import Cart
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Product, Category
from coupons.models import Coupon
from django.utils import timezone
from datetime import timedelta
from coupons.views import coupon_apply


class Testurls(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        middleware = SessionMiddleware(get_response=self.request)
        middleware.process_request(self.request)
        self.request.session.save()
        self.request.method = "POST"

        self.cart_obj = Cart(self.request)

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

        self.product_id_str = str(self.product.id)

        self.valid_coupon_for_10_percent = Coupon.objects.create(
            code="FUNTEN",
            valid_from=timezone.now() - timedelta(30),
            valid_to=timezone.now() + timedelta(30),
            discount=10,
            active=True,
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

    def create_cart(self, request, product, quantity):
        cart = Cart(request)
        cart.add_product(product, quantity)
        return cart

    def test_initialize_cart_clean_session(self):
        empty_cart = {}
        self.assertEqual(empty_cart, self.cart_obj.cart)

    def test_add_new_product_to_the_cart(self):
        quantity = 21
        self.cart_obj.add_product(self.product, quantity=quantity)
        cart = self.request.session.get(settings.CART_SESSION_ID)

        self.assertEqual(cart[self.product_id_str]["quantity"], quantity)
        self.assertEqual(
            str(self.product.price), cart[self.product_id_str]["price"]
        )

    def test_add_new_product_to_the_cart_without_quantity_sets_default_quantity(
        self,
    ):
        self.cart_obj.add_product(self.product)
        cart = self.request.session.get(settings.CART_SESSION_ID)
        default_quantity = 1

        self.assertEqual(
            default_quantity, cart[self.product_id_str]["quantity"]
        )

    def test_increment_product_quantity_increments_existing_carts_product_quantity_by_one(
        self,
    ):
        quantity = 5
        self.cart_obj.add_product(self.product, quantity=quantity)
        self.cart_obj.increment_product_quantity(self.product)
        cart = self.request.session.get(settings.CART_SESSION_ID)

        self.assertEqual(quantity + 1, cart[self.product_id_str]["quantity"])

    def test_increment_product_quantity_adds_product_with_default_quantity_when_product_not_already_exists_in_cart(
        self,
    ):
        self.cart_obj.increment_product_quantity(self.product)
        cart = self.request.session.get(settings.CART_SESSION_ID)
        default_quantity = 1

        self.assertEqual(
            default_quantity, cart[self.product_id_str]["quantity"]
        )

    def test_change_product_quantity_overwrites_existing_quantity_with_new_quantity(
        self,
    ):
        existing_quantity = 8
        new_quantity = 12

        self.cart_obj.add_product(self.product, quantity=existing_quantity)
        self.cart_obj.change_product_quantity(
            self.product, quantity=new_quantity
        )
        cart = self.request.session.get(settings.CART_SESSION_ID)

        self.assertEqual(new_quantity, cart[self.product_id_str]["quantity"])

    def test_change_product_quantity_adds_product_to_cart_with_quantity_when_product_not_already_exists_in_cart(
        self,
    ):
        new_quantity = 14

        self.cart_obj.change_product_quantity(
            self.product, quantity=new_quantity
        )
        cart = self.request.session.get(settings.CART_SESSION_ID)

        self.assertEqual(new_quantity, cart[self.product_id_str]["quantity"])

    def test_remove_product_deletes_product_from_cart_if_exists(self):
        self.cart_obj.add_product(self.product, quantity=10)
        self.cart_obj.remove_product(self.product)
        cart = self.request.session.get(settings.CART_SESSION_ID)

        empty_cart = {}

        self.assertEqual(empty_cart, cart)

    def test_get_total_price_returns_sum_of_price_of_products_in_cart(self):
        quantity = 9
        self.cart_obj.add_product(self.product, quantity=quantity)
        excepted_total_price = self.product.price * quantity

        self.assertEqual(excepted_total_price, self.cart_obj.get_total_price())

    def test_get_total_price_returns_zero_when_cart_is_empty(self):
        quantity = 9
        self.cart_obj.add_product(self.product, quantity=quantity)
        excepted_total_price = self.product.price * quantity

        self.assertEqual(excepted_total_price, self.cart_obj.get_total_price())

    def test_clear_deletes_session_thus_returns_none(self):
        self.cart_obj.clear()
        self.assertIsNone(self.request.session.get(settings.CART_SESSION_ID))

    def test_coupon_returns_coupon_if_exist(self):
        request = self.get_request(
            method="POST", data={"code": self.valid_coupon_for_10_percent.code}
        )
        coupon_apply(request)
        cart = self.create_cart(request, product=self.product, quantity=2)

        self.assertIsInstance(cart.coupon, Coupon)

    def test_coupon_returns_none_if_coupon_doesnot_exist(self):
        request = self.get_request(
            method="POST",
            data={"code": self.expired_coupon_for_50_percent.code},
        )
        coupon_apply(request)
        cart = self.create_cart(request, product=self.product, quantity=2)

        self.assertIsNone(cart.coupon)

    def test_get_discount_returns_discount_price(self):
        request = self.get_request(
            method="POST", data={"code": self.valid_coupon_for_10_percent.code}
        )
        coupon_apply(request)
        cart = self.create_cart(request, product=self.product, quantity=2)

        discount_price = (self.product.price * 2) * (
            self.valid_coupon_for_10_percent.discount / 100
        )

        self.assertEqual(discount_price, cart.get_discount())

    def test_get_discount_returns_zero_discount_price_when_coupon_invalid(
        self,
    ):
        request = self.get_request(
            method="POST",
            data={"code": self.expired_coupon_for_50_percent.code},
        )
        coupon_apply(request)
        cart = self.create_cart(request, product=self.product, quantity=2)

        self.assertEqual(0, cart.get_discount())

    def test_get_total_price_after_discount(self):
        request = self.get_request(
            method="POST", data={"code": self.valid_coupon_for_10_percent.code}
        )
        coupon_apply(request)
        cart = self.create_cart(request, product=self.product, quantity=2)

        total_price = self.product.price * 2
        discount_price = total_price * (
            self.valid_coupon_for_10_percent.discount / 100
        )
        calucated_discount_price = total_price - discount_price

        self.assertEqual(
            calucated_discount_price,
            cart.get_total_price_after_discount(),
        )
