from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from notifications import notify
from shop.models import SellerProfile,SaleItem,Category,UserBid,Comment, Order, PaymentChoice, SaleItemAdditionalImages
from shop.forms import SaleItemForm, UserBidForm, SellerProfileForm, OrderCheckoutForm, OrderConfirmationForm, \
	DummyItemForm
import re
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from filters import SaleItemFilter

## Custom Decorators

def has_seller_profile(user):
	if user:
		try:
			sellerprofile = user.sellerprofile
			return True
		except AttributeError:
			return False


	return False

######



def index(request,
          template='shop/index.html',
          page_template='shop/item_list.html'):
	f = SaleItem.objects.filter(available=True, deal=True).order_by('-post_time')
	context_dict = {'filter': f, 'page_template': page_template}

	if request.is_ajax():
		template = page_template

	return render_to_response(
		template, context_dict, context_instance=RequestContext(request))


#def category(request, category_name_slug):
#	category = Category.objects.get(slug=category_name_slug)
#	item_list = SaleItem.objects.filter(Q(category=category) | Q(category__parent_category=category)).order_by('-post_time')
#	context_dict = {'category': category, 'items': item_list}
#	return render(request, 'shop/category.html', context_dict)

def category(
		request,
		category_name_slug,
		template='shop/category.html',
		page_template='shop/item_list.html'):

	category = Category.objects.get(slug=category_name_slug)
	item_list = SaleItem.objects.filter((Q(category=category) | Q(category__parent_category=category)),deal=True).order_by('-post_time')
	# f = SaleItemFilter(request.GET, queryset=item_list)
	context_dict = {'category': category, 'items': item_list, 'page_template': page_template, 'filter': item_list}

	if request.is_ajax():
		template = page_template

	return render_to_response(
		template, context_dict, context_instance=RequestContext(request))

def saleitem(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	context_dict = {'item': item}
	context_dict['user'] = request.user
	context_dict['itemcondition'] = item.get_condition_display()
	context_dict['homedelivery'] = item.owner.get_home_delivery_display()
	context_dict['payment'] = PaymentChoice.objects.filter(sellerprofile=item.owner)
	context_dict['additional_images'] = SaleItemAdditionalImages.objects.filter(sale_item=item)
	try:
		highestbid = UserBid.objects.filter(sale_item=item).order_by('-offer_price')[0]
		context_dict['highestbid'] = highestbid
	except:
		pass

	return render(request, 'shop/item.html', context_dict)

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def add_new_item(request):
	if request.method == 'POST':
		form = SaleItemForm(request.POST,request.FILES)

		if form.is_valid():
			item = form.save(commit=False)
			item.owner = request.user.sellerprofile

			if 'image' in request.FILES:
				item.image = request.FILES['image']

			if item.usual_price:
				item.deal = True

			item.save()

			if 'additional_images' in request.FILES:
				for image in request.FILES.getlist('additional_images'):
					SaleItemAdditionalImages.objects.create(image=image, sale_item=item)

			return redirect('shop:item', item.slug)
		else:
			print form.errors

	else:
		form = SaleItemForm()

	return render(request, 'shop/add_new_item.html', {'form': form})




def sellerprofile(request, seller_id):
	sellerprofile = SellerProfile.objects.get(id=seller_id)
	context_dict = {'sellerprofile': sellerprofile}
	return render(request, 'shop/sellerprofile.html', context_dict)

@login_required
def make_bid(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	context_dict = {'item': item}
	try:
		highestbid = UserBid.objects.filter(sale_item=item).order_by('-offer_price')[0]
		context_dict['highestbid'] = highestbid
		min_offer = highestbid.offer_price + 1
		context_dict['min_offer'] = min_offer
	except:
		pass

	try:
		userbid = UserBid.objects.get(user=request.user,sale_item=item)

	except UserBid.DoesNotExist:
		userbid = UserBid(user=request.user,sale_item=item)


	if request.method == 'POST':
		form = UserBidForm(request.POST, instance=userbid)
		if form.is_valid():
			form.save()
			notify.send(request.user, recipient=item.owner.user, verb=u' made an offer on your item: ', target=item)

			for ubid in item.userbid_set.all():

				if ubid.user == request.user:
					continue

				notify.send(request.user, recipient=ubid.user, verb=u' bid on an item that you bid on', target=item)

			return redirect('shop:item', item.slug)

		else:
			print form.errors
			context_dict['form'] = form

	else:
		form = UserBidForm()
		context_dict['form'] = form
		return render(request, 'shop/makebid.html', context_dict)

@login_required
def create_sellerprofile(request):
	if request.method=='POST':
		form = SellerProfileForm(request.POST, request.FILES)
		if form.is_valid():
			sellerprofile = form.save(commit=False)
			sellerprofile.user = request.user
			if 'image' in request.FILES:
				sellerprofile.image = request.FILES['image']

			sellerprofile.save()
			form.save_m2m()
			return redirect('index')
		else:
			print form.errors
	else:
		form = SellerProfileForm()
	return render(request, 'shop/create_sellerprofile.html', {'form': form})

@login_required
def item_cart(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	context_dict = {'item': item}
	return render(request, 'shop/item_cart.html', context_dict)

@login_required
def checkout(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	if not item.available:
		return redirect('index')

	context_dict = {'item':item, 'user': request.user}
	context_dict['payment'] = PaymentChoice.objects.filter(sellerprofile=item.owner)
	if request.method=='POST':
		form = OrderCheckoutForm(request.POST)
		context_dict['form'] = form
		if form.is_valid():
			order = form.save(commit=False)
			order.buyer = request.user
			order.buy_item = item
			order.save()
			return redirect('shop:confirmation', order.id)
		else:
			print form.errors
	else:
		form = OrderCheckoutForm()
		context_dict['form'] = form
	return render(request, 'shop/checkout.html', context_dict)


@login_required
def confirmation(request, order_id):
	try:
		order = Order.objects.get(id=order_id)
		if request.user != order.buyer:
			return redirect('index')

		item = order.buy_item
		context_dict = {'order': order, 'item':item}
		if request.method=='POST':
			form = OrderConfirmationForm(request.POST, instance=order)
			context_dict['form'] = form
			if form.is_valid():
				confirmorder = form.save(commit=False)
				confirmorder.confirmed = True
				confirmorder.save()
				confirmorder.buy_item.available = False
				confirmorder.buy_item.save(update_fields=['available'])
				notify.send(request.user, recipient=item.owner.user, verb=u' placed an order on your item. Go to your dashboard to view your orders.', target=confirmorder)

				return redirect('shop:order', order_id=confirmorder.id)
			else:
				print form.errors

		else:
			form = OrderConfirmationForm()
			context_dict['form'] = form

		return render(request, 'shop/confirmation.html',context_dict)


	except Order.DoesNotExist:
		return redirect('index')

@login_required
def bidcheckout(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	try:
		if request.user != item.accepted_bid.user:
			return redirect('index')
	except AttributeError:
		return redirect('index')

	context_dict = {'item':item, 'user': request.user}
	context_dict['payment'] = PaymentChoice.objects.filter(sellerprofile=item.owner)
	if request.method=='POST':
		form = OrderCheckoutForm(request.POST)
		context_dict['form'] = form
		if form.is_valid():
			order = form.save(commit=False)
			order.buyer = request.user
			order.buy_item = item
			order.save()
			return redirect('shop:confirmation', order.id)
		else:
			print form.errors
	else:
		form = OrderCheckoutForm()
		context_dict['form'] = form
	return render(request, 'shop/bidcheckout.html', context_dict)


@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def acceptbid(request, bid_id):
	bid = UserBid.objects.get(id=bid_id)

	# Users do not have items, SELLERS have items
	try:
		if request.user.sellerprofile != bid.sale_item.owner:
			return redirect('index')
	except:
		return redirect('index')

	if request.method=='POST':
		bid.sale_item.available = False
		bid.sale_item.accepted_bid = bid
		bid.sale_item.save(update_fields=['available','accepted_bid'])
		notify.send(request.user, recipient=bid.user, verb=u' accepted your offer on their item. Click the link to review and checkout ', target=bid)
		return redirect('shop:dashboard')

	context_dict={'item':bid.sale_item, 'bid':bid}
	return render(request, 'shop/acceptbid.html', context_dict )

@login_required
def myorders(request):
	context_dict = {'current_orders':Order.objects.filter(buyer=request.user, confirmed=True, completed=False)}
	return render(request, 'shop/myorders.html',context_dict)

@login_required
def order(request, order_id):
	try:
		order = Order.objects.get(id=order_id)
		try:
			if request.user != order.buyer:
				if request.user.sellerprofile != order.buy_item.owner:
					return redirect('index')

			if not order.confirmed:
				return redirect('index')
		except AttributeError:
			return redirect('index')

		item = order.buy_item
		context_dict = {'order': order, 'item':item}
		if request.method=='POST':
			order.completed = True
			order.save(update_fields=['completed'])
			return redirect('shop:dashboard')
		else:
			return render(request, 'shop/order.html',context_dict)

	except Order.DoesNotExist:
		return redirect('index')




# dashboard views ########################### ###############################

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def sellerdashboard(request):
	current_items_count = SaleItem.objects.filter(owner=request.user.sellerprofile,available=True).count()
	past_items_count = SaleItem.objects.filter(owner=request.user.sellerprofile, available=False).count()
	current_orders_count = Order.objects.filter(buy_item__owner=request.user.sellerprofile, completed=False).count()
	past_orders_count = Order.objects.filter(buy_item__owner=request.user.sellerprofile, completed=True).count()
	context_dict = {'sellerprofile':request.user.sellerprofile, 'current_items_count':current_items_count,
					'past_items_count':past_items_count,'current_orders_count':current_orders_count,
					'past_orders_count':past_orders_count}
	return render(request, 'shop/dashboard.html', context_dict)

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def dashboard_current_items(request):
	context_dict = {'current_items': SaleItem.objects.filter(owner=request.user.sellerprofile,available=True).order_by('post_time')}
	return render(request, 'shop/dashboard_current_items.html', context_dict)

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def dashboard_past_items(request):
	context_dict = {'past_items': SaleItem.objects.filter(owner=request.user.sellerprofile, available=False).order_by('post_time')}
	return render(request, 'shop/dashboard_past_items.html',context_dict)

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def dashboard_current_orders(request):
	context_dict = {'current_orders':Order.objects.filter(buy_item__owner=request.user.sellerprofile, confirmed=True, completed=False)}
	return render(request, 'shop/dashboard_current_orders.html',context_dict)

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def dashboard_past_orders(request):
	context_dict = {'past_orders':Order.objects.filter(buy_item__owner=request.user.sellerprofile, confirmed=True, completed=True) }
	return render(request, 'shop/dashboard_past_orders.html', context_dict)

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def removeitem(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	try:
		if request.user.sellerprofile != item.owner:
			return redirect('index')
	except AttributeError:
		return redirect('index')

	if request.method=='POST':
		item.available = False
		item.save(update_fields=['available'])
		return redirect('shop:dashboard_current_items')

	return redirect('shop:dashboard')

@login_required
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def reactivateitem(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	try:
		if request.user.sellerprofile != item.owner:
			return redirect('index')
	except AttributeError:
		return redirect('index')

	if request.method=='POST':
		item.available = True
		item.save(update_fields=['available'])
		return redirect('shop:dashboard_past_items')

	return redirect('shop:dashboard')




# search view  ###############################



def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
		and grouping quoted words together.
		Example:

		>>> normalize_query('  some random  words "with   quotes  " and   spaces')
		['some', 'random', 'words', 'with quotes', 'and', 'spaces']

	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
		aims to search keywords within a model by testing the given search fields.

	'''
	query = None # Query to search for every search term
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query

def search(request):
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

		entry_query = get_query(query_string, ['title', 'description',])

		found_entries = SaleItem.objects.filter(entry_query).order_by('post_time')

	return render_to_response('shop/search_results.html',
						  { 'query_string': query_string, 'found_entries': found_entries },
						  context_instance=RequestContext(request))


# 404

def handler404(request):
	response = render_to_response("main/404.html", {},
								  context_instance=RequestContext(request))
	response.status_code = 404
	return response




## the dummy hack view

@user_passes_test(lambda u: u.is_superuser)
@user_passes_test(has_seller_profile, login_url='/shop/create_sellerprofile')
def add_dummyitem(request):
	if request.method == 'POST':
		form = DummyItemForm(request.POST,request.FILES)

		if form.is_valid():
			item = form.save(commit=False)
			item.owner = request.user.sellerprofile

			if 'image' in request.FILES:
				item.image = request.FILES['image']

			if item.usual_price:
				item.deal = True

			item.save()

			if 'additional_images' in request.FILES:
				for image in request.FILES.getlist('additional_images'):
					SaleItemAdditionalImages.objects.create(image=image, sale_item=item)

			return redirect('shop:add_dummyitem')
		else:
			print form.errors

	else:
		form = DummyItemForm()

	return render(request, 'shop/add_dummyitem.html', {'form': form})