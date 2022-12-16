from orders.models import Order
from orders.views import order_create
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from cart.cart import Cart
from shop.models import Product, Category
from coupons.models import Coupon
from django.utils import timezone
from coupons.views import coupon_apply
from datetime import timedelta


class TestModelMethods(TestCase):
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
        cart.coupon_id = self.valid_coupon_for_10_percent.id
        return cart

    def test_get_total_cost(self):
        request = self.get_request(
            method="POST",
            data={
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.ocm",
                "address": "132, Main street, New town",
                "postal_code": "782032",
                "city": "Gowtham city",
            },
        )
        self.create_cart(request, self.product, 2)
        order_create(request)
        order = Order.objects.filter(id=1)[0]

        total_cost = self.product.price * 2
        discount_price = total_cost * (order.discount / 100)
        excepted_total_cost = total_cost - discount_price

        self.assertEqual(excepted_total_cost, order.get_total_cost())

    def test_get_total_cost_with_coupon(self):
        request = self.get_request(
            method="POST",
            data={
                "code": self.valid_coupon_for_10_percent.code,
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.ocm",
                "address": "132, Main street, New town",
                "postal_code": "782032",
                "city": "Gowtham city",
            },
        )
        coupon_apply(request)
        self.create_cart(request, product=self.product, quantity=2)
        order_create(request)
        order = Order.objects.filter(id=1)[0]

        total_cost = self.product.price * 2
        discount_price = total_cost * (order.discount / 100)
        excepted_total_cost = total_cost - discount_price

        self.assertEqual(excepted_total_cost, order.get_total_cost())
