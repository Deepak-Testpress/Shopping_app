from django.test import TestCase
from cart.forms import CartAddProductForm


class TestForms(TestCase):
    def test_adding_product_with_available_quantity_succeeds(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 20,
            }
        )

        self.assertTrue(form.is_valid())

    def test_adding_product_with_unavailable_quantity_fails(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 24,
            }
        )

        self.assertFalse(form.is_valid())

    def test_adding_product_with_invalid_quantity_fails(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 0,
            }
        )

        self.assertFalse(form.is_valid())

    def test_adding_product_to_cart_fails_for_non_integer_quantity(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 3.0,
            }
        )

        self.assertFalse(form.is_valid())
