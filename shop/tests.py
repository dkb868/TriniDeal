from django.test import TestCase
from django.core.urlresolvers import reverse
from shop.forms import SaleItemForm
from shop.models import Category, SellerProfile, SaleItem
from django.contrib.auth.models import User


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
        testuser = User.objects.create(username='testuser')
        testcat = Category.objects.create(name='testcat')
        testseller = SellerProfile.objects.create(user=testuser)
        testitem = SaleItem.objects.create(	owner = testseller, title = 'testtitle',
                                            condition = 'NEW', payment_type = 'COD',
                                            category = testcat )

        response = self.client.get(reverse('shop:item', kwargs={'item_slug':'testtitle'}))
        self.assertEqual(response.status_code, 200)

class AddNewItemViewTests(TestCase):

    def test_valid_saleitem_creation(self):

        testcat = Category.objects.create(name='testcat')
        data = {'title': 'testtitle','condition': 'NEW',
                'description': 'its legit',
                'asking_price': 334334,
                'payment_type':'COD',
                'negotiable': True,
                'expiration_date': '4/4/2015',
                'category': testcat.id,
                'refundable': True,
                'home_delivery': True}

        form = SaleItemForm(data=data)
        print form.errors
        self.assertTrue(form.is_valid())

        # Need SellerProfile to actually test the posting