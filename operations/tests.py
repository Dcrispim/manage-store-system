from django.test import TestCase
from .models import *

# Create your tests here.

class TestModelProduct(TestCase):
    def setUp(self):
        self.product = Product.create(
                                        name='test_produc_name', 
                                        brand='test_product_brand',
                                        unit='test_product_unit'
                                    )

    def test_str_product_must_be_return_test_product_name(self):
        expected = 'test_produc_name'
        result = str(self.product)
        self.assertEqual(expected, result)