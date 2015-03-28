from django.test import TestCase, Client, TransactionTestCase
from django.core.urlresolvers import reverse
from notifications.models import Notification
from shop.forms import SaleItemForm, UserBidForm, SellerProfileForm, OrderCheckoutForm, OrderConfirmationForm
from shop.models import Category, SellerProfile, SaleItem, UserBid, PaymentChoice, Order
from django.contrib.auth.models import User


## Creator functions

def add_user(username):
	u = User.objects.create_user(username=username)
	return u

def add_sellerprofile(user):
	sp = SellerProfile.objects.create(user=user,home_delivery='NONE')
	return sp

def add_cat(name):
	c = Category.objects.create(name=name)
	return c

def add_item(title, asking_price, category, owner, condition='NEW',):
	item = SaleItem.objects.create(title=title,asking_price=asking_price,
								   category=category, owner=owner,
									condition=condition,)
	return item

## Test Classes

class IndexViewTests(TestCase):

	def test_index_with_no_items(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['items'], [])

	def test_index_with_an_item(self):
		testuser = add_user('testuser')
		testusersp = add_sellerprofile(testuser)
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=testusersp)
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['items'], ['<SaleItem: testitem>'])


class CategoryViewTests(TestCase):

	def test_category_with_no_items(self):
		testcat = add_cat('testcat')
		response = self.client.get(reverse('shop:category', kwargs={'category_name_slug':'testcat'}))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['items'], [])

	def test_index_with_an_item(self):
		testuser = add_user('testuser')
		testusersp = add_sellerprofile(testuser)
		testcat = add_cat('testcat')
		testcat2 = add_cat('nottestcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=testusersp)
		testitem2 = add_item(title='testitem2',asking_price=100,
							 category=testcat2,owner=testusersp)
		response = self.client.get(reverse('shop:category', kwargs={'category_name_slug':'testcat'}))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['items'], ['<SaleItem: testitem>'])

class SaleItemViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_saleitem_page(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='test item',asking_price=100,
							category=testcat,owner=self.testusersp)

		response = self.c.get(reverse('shop:item', kwargs={'item_slug':'test-item'}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['item'], testitem)

class AddNewItemViewTests(TestCase):
	def setUp(self):
		testuser = User.objects.create_user(username='testuser',password='password')
		testusersp = add_sellerprofile(testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_valid_saleitem_creation(self):

		testcat = add_cat('testcat')
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
		response = self.c.post(reverse('shop:add_new_item'), data)
		self.assertEqual(response.status_code, 302)

class SellerProfileViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_sellerprofile_page_working(self):
		response = self.c.get(reverse('shop:sellerprofile', kwargs={'seller_id':self.testusersp.id}))
		self.assertEqual(response.status_code, 200)

class MakeBidViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_valid_make_bid_form(self):
		data = {'offer_price':100}
		form = UserBidForm(data=data)
		print form.errors
		self.assertTrue(form.is_valid())

		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		response = self.c.post(reverse('shop:makebid', kwargs={'item_slug':'testitem'}),data=data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Notification.objects.count(), 1)

	# Tests to see if users with previous bids can make new ones
	def test_valid_update_bid_form(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		UserBid.objects.create(user=self.testuser,sale_item=testitem,offer_price=200)
		# Checking the bid before the form
		previousbid = UserBid.objects.get(user=self.testuser,sale_item=testitem)
		self.assertEqual(previousbid.offer_price, 200)
		data = {'offer_price':300}
		form = UserBidForm(data=data)
		print form.errors
		self.assertTrue(form.is_valid())
		response = self.c.post(reverse('shop:makebid', kwargs={'item_slug':'testitem'}),data=data)
		self.assertEqual(response.status_code, 302)
		# Checking the bid after the form
		updatedbid = UserBid.objects.get(user=self.testuser,sale_item=testitem)
		self.assertEqual(updatedbid.offer_price, 300)
		self.assertEqual(Notification.objects.count(), 1)


class CreateSellerProfileViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)
		self.cash = PaymentChoice.objects.create(description='cash')

	def tearDown(self):
		self.c.logout()

	def test_valid_sellerprofile_creation(self):
		data = {
			'seller_name': 'testname','location': 'Heaven',
			'phone_number': 12312352,'payment_type': [self.cash.pk],
			'home_delivery': 'ALL','meetup': True,
			'details': 'Blahblah',
			}
		form = SellerProfileForm(data=data)
		print form.errors
		self.assertTrue(form.is_valid())
		response = self.c.post(reverse('shop:create_sellerprofile'),data=data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(SellerProfile.objects.count(), 1)

class ItemCartViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_valid_item_cart_creation(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		response = self.c.get(reverse('shop:item_cart', kwargs={'item_slug':'testitem'}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual((response.context['item']), testitem)

class CheckoutViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)
		self.cash = PaymentChoice.objects.create(description='cash')

	def tearDown(self):
		self.c.logout()

	def test_valid_checkout(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)

		data = {'meetuploc': 'pielantis',
				'phone': 234243242,
				'paymentmethod': self.cash.pk,
				'additionalinfo': 'spam',}
		form = OrderCheckoutForm(data=data)
		self.assertTrue(form.is_valid)
		response = self.c.post(reverse('shop:checkout', kwargs={'item_slug':'testitem'}), data=data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Order.objects.count(), 1)

	def test_page_works_when_item_available(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		response = self.c.get(reverse('shop:checkout', kwargs={'item_slug':'testitem'}))
		self.assertEqual(response.status_code, 200)


	def test_redirect_when_item_unavailable(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		testitem.available = False
		testitem.save(update_fields=['available'])

		response = self.c.get(reverse('shop:checkout', kwargs={'item_slug':'testitem'}))
		self.assertEqual(response.status_code, 302)


class BidCheckoutViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)
		self.cash = PaymentChoice.objects.create(description='cash')

	def tearDown(self):
		self.c.logout()

	def test_valid_bidcheckout(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		testbid = UserBid.objects.create(user=self.testuser,sale_item=testitem,offer_price=200)
		testitem.available = False
		testitem.accepted_bid = testbid
		testitem.save()

		data = {'meetuploc': 'pielantis',
				'phone': 234243242,
				'paymentmethod': self.cash.pk,
				'additionalinfo': 'spam',}
		form = OrderCheckoutForm(data=data)
		self.assertTrue(form.is_valid)
		response = self.c.post(reverse('shop:bidcheckout', kwargs={'item_slug':'testitem'}), data=data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Order.objects.count(), 1)

	def test_page_works_when_user_is_accepted_bid_user(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		testbid = UserBid.objects.create(user=self.testuser,sale_item=testitem,offer_price=200)
		testitem.available = False
		testitem.accepted_bid = testbid
		testitem.save()
		response = self.c.get(reverse('shop:bidcheckout', kwargs={'item_slug':'testitem'}))
		self.assertEqual(response.status_code, 200)


	def test_redirect_when_user_is_not_accepted_bid_user(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		testitem.available = False
		testitem.save(update_fields=['available'])

		response = self.c.get(reverse('shop:bidcheckout', kwargs={'item_slug':'testitem'}))
		self.assertEqual(response.status_code, 302)



class ConfirmationViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)
		self.testcat = add_cat('testcat')
		self.cash = PaymentChoice.objects.create(description='cash')
		self.testitem = add_item(title='testitem',asking_price=100,
							category=self.testcat,owner=self.testusersp)
		self.order = Order.objects.create(buyer=self.testuser,meetuploc='pielantis',
										  phone=12313132,paymentmethod=self.cash,buy_item=self.testitem)
		self.testuser2 = User.objects.create_user(username='testuser2',password='password')
		self.d = Client()
		self.d.login(username='testuser2',password='password')
		self.assertTrue(self.d.login)

	def tearDown(self):
		self.c.logout()

	def test_valid_order_confirmation(self):

		# Checking the agreetoterms and confirmed before the form
		self.assertFalse(self.order.agreetoterms)
		self.assertFalse(self.order.confirmed)
		self.assertTrue(self.order.buy_item.available)
		data = {'agreetoterms': True}
		form = OrderConfirmationForm(data=data)
		self.assertTrue(form.is_valid)
		response = self.c.post(reverse('shop:confirmation', kwargs={'order_id': self.order.id}), data=data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Order.objects.count(), 1)
		orderafter = Order.objects.get(buyer=self.testuser,meetuploc='pielantis',
									   phone=12313132,paymentmethod=self.cash,buy_item=self.testitem)
		# Checking the agreetoterms and confirmed after the form
		self.assertTrue(orderafter.agreetoterms)
		self.assertTrue(orderafter.confirmed)
		# item should now be unavailable
		self.assertFalse(orderafter.buy_item.available)

	def test_confirmation_available_to_user_who_is_the_order_buyer(self):
		response = self.c.get(reverse('shop:confirmation', kwargs={'order_id': self.order.id}))
		self.assertEqual(response.status_code, 200)

	def test_confirmation_unavailable_to_user_who_is_not_the_order_buyer(self):
		response = self.d.get(reverse('shop:confirmation', kwargs={'order_id': self.order.id}))
		self.assertEqual(response.status_code, 302)

class AcceptBidViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)
	def tearDown(self):
		self.c.logout()

	def test_valid_accept_bid(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		self.assertTrue(testitem.available)
		testbid = UserBid.objects.create(user=self.testuser,sale_item=testitem,offer_price=200)
		response = self.c.post(reverse('shop:acceptbid', kwargs={'bid_id':testbid.id}))
		self.assertEqual(response.status_code, 302)
		testitemafter = SaleItem.objects.get(slug='testitem')
		self.assertEqual(testitemafter.accepted_bid, testbid)
		self.assertFalse(testitemafter.available)


	def test_item_owner_can_access_accept_bid_view(self):
		testcat = add_cat('testcat')
		testitem = add_item(title='testitem',asking_price=100,
							category=testcat,owner=self.testusersp)
		self.assertTrue(testitem.available)
		testbid = UserBid.objects.create(user=self.testuser,sale_item=testitem,offer_price=200)
		response = self.c.get(reverse('shop:acceptbid', kwargs={'bid_id':testbid.id}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['bid'], testbid)


# Dashboard tests
class SellerProfileDashboardViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password',
											first_name='test',last_name='user')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_dashboard_page_working(self):
		response = self.c.get(reverse('shop:dashboard'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual((response.context['sellerprofile']), self.testusersp)
		self.assertEqual((response.context['current_items_count']), 0)
		self.assertEqual((response.context['past_items_count']), 0)
		self.assertEqual((response.context['current_orders_count']), 0)
		self.assertEqual((response.context['past_orders_count']), 0)

class DashboardCurrentItemsViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password',
											first_name='test',last_name='user')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_dashboard_current_items_page_working(self):
		response = self.c.get(reverse('shop:dashboard_current_items'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual((response.context['current_items']), [])

class DashboardPastItemsViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password',
											first_name='test',last_name='user')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_dashboard_past_items_page_working(self):
		response = self.c.get(reverse('shop:dashboard_past_items'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual((response.context['past_items']), [])


class DashboardCurrentOrdersViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password',
											first_name='test',last_name='user')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_dashboard_current_orders_page_working(self):
		response = self.c.get(reverse('shop:dashboard_current_orders'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual((response.context['current_orders']), [])

class DashboardPastOrdersViewTests(TestCase):
	def setUp(self):
		self.testuser = User.objects.create_user(username='testuser',password='password',
											first_name='test',last_name='user')
		self.testusersp = add_sellerprofile(self.testuser)
		self.c = Client()
		self.c.login(username='testuser',password='password')
		self.assertTrue(self.c.login)

	def tearDown(self):
		self.c.logout()

	def test_dashboard_past_orders_page_working(self):
		response = self.c.get(reverse('shop:dashboard_past_orders'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual((response.context['past_orders']), [])