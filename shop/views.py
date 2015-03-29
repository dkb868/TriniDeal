from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from notifications import notify
from shop.models import SellerProfile,SaleItem,Category,UserBid,SaleItemImage,Comment, Order, PaymentChoice
from shop.forms import SaleItemForm, UserBidForm, SellerProfileForm, OrderCheckoutForm, OrderConfirmationForm


def index(request):
	item_list = SaleItem.objects.filter(available=True).order_by('post_time')[:9]
	context_dict = {'items': item_list}
	return render(request, 'shop/index.html', context_dict)


def category(request, category_name_slug):
	category = Category.objects.get(slug=category_name_slug)
	item_list = SaleItem.objects.filter(category=category).order_by('post_time')[:9]
	context_dict = {'category': category, 'items': item_list}
	return render(request, 'shop/category.html', context_dict)

def saleitem(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	context_dict = {'item': item}
	context_dict['user'] = request.user
	context_dict['itemcondition'] = item.get_condition_display()
	context_dict['homedelivery'] = item.owner.get_home_delivery_display()
	context_dict['payment'] = PaymentChoice.objects.filter(sellerprofile=item.owner)
	try:
		highestbid = UserBid.objects.filter(sale_item=item).order_by('-offer_price')[0]
		context_dict['highestbid'] = highestbid
	except:
		pass

	return render(request, 'shop/item.html', context_dict)

def add_new_item(request):
	if request.method == 'POST':
		form = SaleItemForm(request.POST)

		if form.is_valid():
			item = form.save(commit=False)
			item.owner = request.user.sellerprofile
			item.save()
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


def make_bid(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	context_dict = {'item': item}
	try:
		highestbid = UserBid.objects.filter(sale_item=item).order_by('-offer_price')[0]
		context_dict['highestbid'] = highestbid
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
			notify.send(request.user, recipient=item.owner.user, verb=u'Made an offer on your item: ', target=item)
			return redirect('shop:item', item.slug)

		else:
			print form.errors
			context_dict['form'] = form

	else:
		form = UserBidForm()
		context_dict['form'] = form
		return render(request, 'shop/makebid.html', context_dict)

def create_sellerprofile(request):
	if request.method=='POST':
		form = SellerProfileForm(request.POST)
		if form.is_valid():
			sellerprofile = form.save(commit=False)
			sellerprofile.user = request.user
			sellerprofile.save()
			form.save_m2m()
			return redirect('index')
		else:
			print form.errors
	else:
		form = SellerProfileForm()
	return render(request, 'shop/create_sellerprofile.html', {'form': form})

def item_cart(request, item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	context_dict = {'item': item}
	return render(request, 'shop/item_cart.html', context_dict)

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
				return redirect('index')
			else:
				print form.errors

		else:
			form = OrderConfirmationForm()
			context_dict['form'] = form

		return render(request, 'shop/confirmation.html',context_dict)


	except Order.DoesNotExist:
		return redirect('index')

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
		return redirect('shop:dashboard')

	context_dict={'item':bid.sale_item, 'bid':bid}
	return render(request, 'shop/acceptbid.html', context_dict )

def myorders(request):
	context_dict = {'current_orders':Order.objects.filter(buyer=request.user, completed=False)}
	return render(request, 'shop/myorders.html',context_dict)

def order(request, order_id):
	try:
		order = Order.objects.get(id=order_id)
		try:
			if request.user != order.buyer:
				if request.user.sellerprofile != order.buy_item.owner:
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


# dashboard views

def sellerdashboard(request):
	current_items_count = SaleItem.objects.filter(owner=request.user.sellerprofile,available=True).count()
	past_items_count = SaleItem.objects.filter(owner=request.user.sellerprofile, available=False).count()
	current_orders_count = Order.objects.filter(buy_item__owner=request.user.sellerprofile, completed=False).count()
	past_orders_count = Order.objects.filter(buy_item__owner=request.user.sellerprofile, completed=True).count()
	context_dict = {'sellerprofile':request.user.sellerprofile, 'current_items_count':current_items_count,
					'past_items_count':past_items_count,'current_orders_count':current_orders_count,
					'past_orders_count':past_orders_count}
	return render(request, 'shop/dashboard.html', context_dict)

def dashboard_current_items(request):
	context_dict = {'current_items': SaleItem.objects.filter(owner=request.user.sellerprofile,available=True).order_by('post_time')}
	return render(request, 'shop/dashboard_current_items.html', context_dict)

def dashboard_past_items(request):
	context_dict = {'past_items': SaleItem.objects.filter(owner=request.user.sellerprofile, available=False).order_by('post_time')}
	return render(request, 'shop/dashboard_past_items.html',context_dict)

def dashboard_current_orders(request):
	context_dict = {'current_orders':Order.objects.filter(buy_item__owner=request.user.sellerprofile, completed=False)}
	return render(request, 'shop/dashboard_current_orders.html',context_dict)

def dashboard_past_orders(request):
	context_dict = {'past_orders':Order.objects.filter(buy_item__owner=request.user.sellerprofile, completed=True) }
	return render(request, 'shop/dashboard_past_orders.html', context_dict)

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