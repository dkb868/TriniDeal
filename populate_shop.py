import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manicou.settings')

import django
django.setup()

from shop.models import SellerProfile, Category, SaleItem


def populate():

    shopowner = SellerProfile.objects.get_or_create()[0]
    # Multiple categories to be added later
    testcat = Category.objects.get_or_create(name="testcat")[0]
    def add_item(title,asking_price, condition='NEW', payment_type='COD', category=testcat,owner=shopowner):
        item = SaleItem.objects.create(title=title,asking_price=asking_price,
                                           condition=condition, payment_type=payment_type,
                                           category=category, owner=owner)
        return item


    add_item(title='Gold Necklace',asking_price='1000')
    add_item(title='FIFA 2015',asking_price='500')
    add_item(title='Fake Gold Necklace',asking_price='600')
    add_item(title='PS3',asking_price='3100')
    add_item(title='Legit Sofa',asking_price='5100')
    add_item(title='Jimi Hendrix Guitar',asking_price='7100')
    add_item(title='Pet Manicou',asking_price='120')
    add_item(title='LOL RP Cards',asking_price='1300')
    add_item(title='Yo mama',asking_price='1130')
    add_item(title='Game of Trolls',asking_price='1300')
    add_item(title='Samsung Galaxy S6',asking_price='1003')
    add_item(title='Nintendo Gamecube',asking_price='4030')
    add_item(title='Crusty Old Socks',asking_price='500')
    add_item(title='Phone Battery',asking_price='6400')
    add_item(title='Wooden Cupboard',asking_price='1200')
    add_item(title='Homemade Pr0ns',asking_price='1240')
    add_item(title='Homemade Necklace',asking_price='100')
    add_item(title='PS2 Call of Duty',asking_price='1400')
    add_item(title='The Notebook',asking_price='50')
    add_item(title='Nikon DC3100 Camera',asking_price='10')
    add_item(title='Laptop Bag',asking_price='12300')
    add_item(title='Fake Jansport',asking_price='5300')
    add_item(title='CAPE Math Textbook',asking_price='110')
    add_item(title='Bed Sheets',asking_price='12300')
    add_item(title='My Soul',asking_price='12400')
    add_item(title='Freshly Made Paint',asking_price='9001')
    add_item(title='A Rock',asking_price='69')
    add_item(title='Mp5 player',asking_price='113')
    add_item(title='Fancy Lighter',asking_price='35100')
    add_item(title='Perfume',asking_price='134500')
    add_item(title='Levi Jeans',asking_price='1030')
    add_item(title='Swag T-Shirt',asking_price='1030')
    add_item(title='OBEY Cap',asking_price='1050')
    add_item(title='Iphone Charger',asking_price='1500')
    add_item(title='Black Converse',asking_price='1040')
    add_item(title='Ticket to Moon',asking_price='1070')


    for item in SaleItem.objects.all():
        print str(item)

if __name__ == '__main__':
    print "Starting shop population script..."
    populate()


