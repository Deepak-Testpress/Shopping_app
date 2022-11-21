from django.test import TestCase
from cart.forms import CartAddProductForm


class TestForms(TestCase):
    def test_cart_add_product_validates_true_with_quantity_not_exceeding_choice_range(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 20,
            }
        )

        self.assertTrue(form.is_valid())

    def test_cart_add_product_validates_false_with_quantity_exceeding_choice_range(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 24,
            }
        )

        self.assertFalse(form.is_valid())

    def test_cart_add_product_validates_false_with_quantity_undervalue_choice_range(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 0,
            }
        )

        self.assertFalse(form.is_valid())

    def test_cart_add_product_validates_false_with_quantity_non_integer_choice_value(
        self,
    ):
        form = CartAddProductForm(
            data={
                "quantity": 3.0,
            }
        )

        self.assertFalse(form.is_valid())
