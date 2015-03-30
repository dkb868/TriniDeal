import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manicou.settings')

import django
django.setup()

from shop.models import SellerProfile, Category, SaleItem, PaymentChoice
from django.contrib.auth.models import User
from PIL import Image

def populate():
	shopowner = SellerProfile.objects.get(user__username='blacknyancat')
	def add_item(title,asking_price,  category, condition='NEW',owner=shopowner,image='/sale_item_images/example.jpg'):
		item = SaleItem.objects.create(title=title,asking_price=asking_price,category=category,
										   condition=condition,
										   owner=owner,image=image)
		return item

	homemade = Category.objects.get(name='Homemade Crafts')
	books = Category.objects.get(name='Books')
	clothing = Category.objects.get(name='Clothing, Shoes & Accessories')
	jewellery = Category.objects.get(name='Jewellery')
	electronics = Category.objects.get(name='Electronics')
	games = Category.objects.get(name='Video Games')
	music = Category.objects.get(name='Musical Instruments & Accessories')
	miscellaneous = Category.objects.get(name='Miscellaneous')

	mensclothing = Category.objects.get(name='Men\'s Clothes')
	womensclothing = Category.objects.get(name='Women\'s Clothes')
	childrensclothing = Category.objects.get(name='Children\'s Clothes')
	accessoriesclothing = Category.objects.get(name='Accessories')

	cellphones = Category.objects.get(name='Cell Phones and Accessories')
	cameras = Category.objects.get(name='Cameras')
	computers = Category.objects.get(name='Desktops and Laptops')
	tablets = Category.objects.get(name='Tablets')
	otherelectronics = Category.objects.get(name='Other')
	ps4 = Category.objects.get(name='PS4')
	ps3 = Category.objects.get(name='PS3')
	x360 = Category.objects.get(name='XBOX 360')
	xbone = Category.objects.get(name='XBOX One')
	otherconsoles = Category.objects.get(name='Other Consoles')


	add_item(title='Gold Necklace',asking_price='1000',category=homemade)
	add_item(title='FIFA 2015',asking_price='500',category=homemade)
	add_item(title='Fake Gold Necklace',asking_price='600',category=homemade)
	add_item(title='PS3',asking_price='3100',category=homemade)
	add_item(title='Legit Sofa',asking_price='5100',category=homemade)
	add_item(title='Jimi Hendrix Guitar',asking_price='7100',category=homemade)
	add_item(title='Pet Manicou',asking_price='120',category=homemade)
	add_item(title='LOL RP Cards',asking_price='1300',category=homemade)
	add_item(title='Yo mama',asking_price='1130',category=homemade)
	add_item(title='Game of Trolls',asking_price='1300',category=books)
	add_item(title='Samsung Galaxy S6',asking_price='1003',category=books)
	add_item(title='Nintendo Gamecube',asking_price='4030',category=books)
	add_item(title='Crusty Old Socks',asking_price='500',category=books)
	add_item(title='Phone Battery',asking_price='6400',category=books)
	add_item(title='Wooden Cupboard',asking_price='1200',category=books)
	add_item(title='Homemade Pr0ns',asking_price='1240',category=books)
	add_item(title='Homemade Necklace',asking_price='100',category=books)
	add_item(title='PS2 Call of Duty',asking_price='1400',category=books)
	add_item(title='The Notebook',asking_price='50',category=mensclothing)
	add_item(title='Nikon DC3100 Camera',asking_price='10',category=mensclothing)
	add_item(title='Laptop Bag',asking_price='12300',category=mensclothing)
	add_item(title='Fake Jansport',asking_price='5300',category=womensclothing)
	add_item(title='CAPE Math Textbook',asking_price='110',category=womensclothing)
	add_item(title='Bed Sheets',asking_price='12300',category=womensclothing)
	add_item(title='My Soul',asking_price='12400',category=childrensclothing)
	add_item(title='Freshly Made Paint',asking_price='9001',category=childrensclothing)
	add_item(title='A Rock',asking_price='69',category=childrensclothing)
	add_item(title='Mp5 player',asking_price='113',category=jewellery)
	add_item(title='Fancy Lighter',asking_price='35100',category=jewellery)
	add_item(title='Perfume',asking_price='134500',category=jewellery)
	add_item(title='Levi Jeans',asking_price='1030',category=jewellery)
	add_item(title='Swag T-Shirt',asking_price='1030',category=jewellery)
	add_item(title='OBEY Cap',asking_price='1050',category=jewellery)
	add_item(title='Iphone Charger',asking_price='1500',category=jewellery)
	add_item(title='Black Converse',asking_price='1040',category=jewellery)
	add_item(title='Ticket to Moon',asking_price='1070',category=jewellery)
	add_item(title='Mp5 player',asking_price='113',category=cellphones)
	add_item(title='Fancy Lighter',asking_price='35100',category=cellphones)
	add_item(title='Perfume',asking_price='134500',category=cellphones)
	add_item(title='Levi Jeans',asking_price='1030',category=cellphones)
	add_item(title='Swag T-Shirt',asking_price='1030',category=cellphones)
	add_item(title='OBEY Cap',asking_price='1050',category=cellphones)
	add_item(title='Iphone Charger',asking_price='1500',category=cameras)
	add_item(title='Black Converse',asking_price='1040',category=cameras)
	add_item(title='Ticket to Moon',asking_price='1070',category=tablets)
	add_item(title='Mp5 player',asking_price='113',category=tablets)
	add_item(title='Fancy Lighter',asking_price='35100',category=tablets)
	add_item(title='Perfume',asking_price='134500',category=tablets)
	add_item(title='Levi Jeans',asking_price='1030',category=ps4)
	add_item(title='Swag T-Shirt',asking_price='1030',category=ps4)
	add_item(title='OBEY Cap',asking_price='1050',category=ps4)
	add_item(title='Iphone Charger',asking_price='1500',category=ps4)
	add_item(title='Black Converse',asking_price='1040',category=x360)
	add_item(title='Ticket to Moon',asking_price='1070',category=x360)
	add_item(title='Mp5 player',asking_price='113',category=ps3)
	add_item(title='Fancy Lighter',asking_price='35100',category=ps3)
	add_item(title='Perfume',asking_price='134500',category=otherconsoles)
	add_item(title='Levi Jeans',asking_price='1030',category=otherconsoles)
	add_item(title='Swag T-Shirt',asking_price='1030',category=otherconsoles)
	add_item(title='OBEY Cap',asking_price='1050',category=music)
	add_item(title='Iphone Charger',asking_price='1500',category=music)
	add_item(title='Black Converse',asking_price='1040',category=music)
	add_item(title='Ticket to Moon',asking_price='1070',category=music)
	add_item(title='OBEY Cap',asking_price='1050',category=music)
	add_item(title='Iphone Charger',asking_price='1500',category=music)
	add_item(title='Black Converse',asking_price='1040',category=music)
	add_item(title='Ticket to Moon',asking_price='1070',category=music)
	add_item(title='OBEY Cap',asking_price='1050',category=music)
	add_item(title='Iphone Charger',asking_price='1500',category=music)
	add_item(title='Black Converse',asking_price='1040',category=music)
	add_item(title='Ticket to Moon',asking_price='1070',category=miscellaneous)
	add_item(title='Ticket to Moon',asking_price='1070',category=miscellaneous)
	add_item(title='Ticket to Moon',asking_price='1070',category=miscellaneous)
	add_item(title='Ticket to Moon',asking_price='1070',category=miscellaneous)


	for item in SaleItem.objects.all():
		print str(item)

if __name__ == '__main__':
	print "Starting shop population script..."
	populate()


