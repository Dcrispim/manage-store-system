from django.test import TestCase
from .models import *

# Create your tests here.

class TestModelProduct(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
                                        name='test_product_name', 
                                        brand='test_product_brand',
                                        unit='test_product_unit'
                                    )

    ##TESTING PARAMETERS
    def test_str_product_must_be_return_test_product_name(self):
        expected = 'test_product_name'
        result = str(self.product)
        self.assertEqual(expected, result)
    
    def test_brand_product_must_be_return_test_product_brand(self):
        expected = 'test_product_brand'
        result = self.product.brand
        self.assertEqual(expected, result)
    
    def test_unit_product_must_be_return_test_product_unit(self):
        expected = 'test_product_unit'
        result = self.product.unit
        self.assertEqual(expected, result)


class TestModelClient(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
                                        name    = 'test_client_name',
                                        cell    = 'test_client_cell',
                                        email   = 'test_client_email',
                                        address = 'test_client_address',
                                        birth   = '2019-05-04'
                                    )

    ##TESTING PARAMETERS
    def test_str_client_must_be_return_test_client_name(self):
        expected = 'test_client_name'
        result = str(self.client)
        self.assertEqual(expected, result)
    
    def test_cell_client_must_be_return_test_client_cell(self):
        expected = 'test_client_cell'
        result = self.client.cell
        self.assertEqual(expected, result)
    
    def test_email_client_must_be_return_test_client_email(self):
        expected = 'test_client_email'
        result = self.client.email
        self.assertEqual(expected, result)
    
    def test_address_client_must_be_return_test_client_address(self):
        expected = 'test_client_address'
        result = self.client.address
        self.assertEqual(expected, result)
    
    def test_birth_client_must_be_return_2019_05_04(self):
        expected = '2019-05-04'
        result = self.client.birth
        self.assertEqual(expected, result)


class TestModelStock(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
                                        name='test_product_name', 
                                        brand='test_product_brand',
                                        unit='test_product_unit'
                                    )
        self.stock = Stock.objects.create(
                                        product    = self.product,
                                        qtd        = 10,
                                        sale_price = 12
                                    )

    ##TESTING PARAMETERS
    def test_str_stock_must_be_return_test_stock_name(self):
        expected = 'test_product_name'
        result = str(self.stock)
        self.assertEqual(expected, result)
    
    # Fix business rules
    def test_qtd_stock_must_be_return_test_stock_qtd(self):
        expected = 10
        result = self.stock.qtd
        self.assertEqual(expected, result)
    
    def test_sale_price_stock_must_be_return_test_stock_sale_price(self):
        expected = 12
        result = self.stock.sale_price
        self.assertEqual(expected, result)
    
    