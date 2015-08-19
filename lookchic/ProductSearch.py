__author__ = 'zoe'

import sys
import models

class Product(object):

    def __init__(self, name, id, brand_id):
        self._productName=name
        if (id>0):
            from models import get_product_detail
            price=get_product_detail(id)
            self._price=price

        if (brand_id>0):
            from models import get_product_brand
            brand=get_product_brand(brand_id)
            self._brand=brand[0]

        self._pic=''

        from models import get_product_link
        urls=get_product_link(id)
        for url in urls:
            self._webUrl.append(url)


    def __init__(self):
        self._productName = ''
        self._price = 0
        self.pic = ''
        self._webUrl = ''


class Products(object):

    def __init__(self):
        self.products=None



from models import *

def SearchProductByKeyword(keyword):
    resultList=[]
    if (keyword is None):
        return None

    keys=keyword.split(' ')

    if (len(keys)>0 and len(keys)==1):
        from models import searchProduct
        #Column: ID, Brand_id, ProductType_ID, Name
        productResult=searchProduct(keys)
