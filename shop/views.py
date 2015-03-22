from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from shop.models import SellerProfile,SaleItem,Category,UserBid,SaleItemImage,Comment
from shop.forms import SaleItemForm, UserBidForm


def index(request):
    item_list = SaleItem.objects.all()
    context_dict = {'items': item_list}
    return render(request, 'main/index.html', context_dict)


def category(request, category_name_slug):
    category = Category.objects.get(slug=category_name_slug)
    item_list = SaleItem.objects.filter(category=category)
    context_dict = {'category': category, 'items': item_list}
    return render(request, 'main/index.html', context_dict)

def saleitem(request, item_slug):
    item = SaleItem.objects.get(slug=item_slug)
    context_dict = {'item': item}

    bidform = UserBidForm()
    context_dict['bidform'] = bidform
    return render(request, 'main/item.html', context_dict)

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




def sellerprofile(request, user_id):
    sellerprofile = User.objects.get(id=user_id).sellerprofile
    context_dict = {'sellerprofile': sellerprofile}
    return render(request, 'main/sellerprofile.html', context_dict)

def sellerdashboard(request):
    context_dict = {'sellerprofile': request.user.sellerprofile}
    return render(request, 'main/dashboard.html', context_dict)

def make_bid(request, item_slug):
    item = SaleItem.objects.get(slug=item_slug)

    try:
        userbid = UserBid.objects.get(user=request.user, sale_item=item)

    except UserBid.DoesNotExist:
        userbid = UserBid(user=request.user,sale_item=item)


    if request.method == 'POST':
        form = UserBidForm(request.POST, instance=userbid)
        if form.is_valid():
            bid = form.save()
            item.current_highest_bid = bid.offer_price
            item.save(update_fields=['current_highest_bid'])
            return redirect('shop:item', item.slug)

        else:
            print form.errors

    else:
        return redirect('index')

