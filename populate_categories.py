import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manicou.settings')

import django
django.setup()

from shop.models import Category


def add_cat(name, parent_category=None):
	c = Category.objects.get_or_create(name=name,parent_category=parent_category)[0]
	return c

def populate():

	# Main Cats
	homemade = add_cat('Homemade Crafts')
	books = add_cat('Books')
	clothing = add_cat('Clothing, Shoes & Accessories')
	jewellery = add_cat('Jewellery')
	#computers = add_cat('Computers')
	electronics = add_cat('Electronics')
	games = add_cat('Video Games')
	#sports = add_cat('Sports')
	music = add_cat('Musical Instruments & Accessories')
	miscellaneous = add_cat('Miscellaneous')

	# Sub Cats
	#add_cat('', homemade)

	#add_cat('', books)

	add_cat('Men\'s Clothes', clothing)
	add_cat('Women\'s Clothes', clothing)
	add_cat('Children\'s Clothes', clothing)
	add_cat('Accessories', clothing)


	#add_cat('', jewellery)

	add_cat('Cell Phones and Accessories', electronics)
	add_cat('Cameras', electronics)
	add_cat('Desktops and Laptops', electronics)
	add_cat('Tablets', electronics)
	add_cat('Other', electronics)

	add_cat('PS4', games)
	add_cat('PS3', games)
	add_cat('XBOX 360', games)
	add_cat('XBOX One', games)
	add_cat('Other Consoles', games)

	#add_cat('', sports)

	#add_cat('', miscellaneous)



	for cat in Category.objects.all():
		print str(cat)

if __name__ == '__main__':
	print "Starting shop category population script..."
	populate()