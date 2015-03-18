from django.test import TestCase
from django.core.urlresolvers import reverse
from shop.models import Category, SellerProfile, SaleItem


class IndexViewTests(TestCase):

    def test_index_with_no_items(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['items'], [])


class CategoryViewTests(TestCase):

    def test_category_with_no_items(self):
        testcat = Category.objects.create(name='testcat')
        response = self.client.get(reverse('shop:category', kwargs={'category_name_slug':'testcat'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['items'], [])

class SaleItemViewTests(TestCase):

    def test_saleitem_page(self):
        testcat = Category.objects.create(name='testcat')
        testseller = SellerProfile.objects.create()
        testitem = SaleItem.objects.create(	owner = testseller, title = 'testtitle',
                                            condition = 'NEW', payment_type = 'COD',
                                            category = testcat )

        response = self.client.get(reverse('shop:item', kwargs={'item_slug':'testtitle'}))
        self.assertEqual(response.status_code, 200)
