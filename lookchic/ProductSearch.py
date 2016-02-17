__author__ = 'zoe'

import sys
import models

class Product(object):
    _productName=""
    _pic_path=""
    _brand=""
    _price=""
    _webUrl=[]
    _saleprice=""
    _color=""

    def __init__(self, name, id, brand_id):
        self._productName=name
        if (id>0):
            from models import get_product_detail
            price=get_product_detail(id)
            self._price=price
            from models import get_product_image
            pic=get_product_image(id)
            self._pic_path=pic

        if (brand_id>0):
            from models import get_product_brand
            brand=get_product_brand(brand_id)
            self._brand=brand
        self._webUrl=''
        from models import get_product_link
        url=get_product_link(id)
        self._webUrl=url

    def __init__(self, name, id, brandName, color, retail, sale, weburl):
        if id > 0:
            self._productName=name
            self._brand=brandName
            self._color=color
            self._price=retail
            self._saleprice=sale
            self._webUrl=weburl
            from models import get_product_image
            self._pic_path=get_product_image(id)
        else:
            return

def SearchProductByKeyword(keyword):
    resultList=[]
    if (keyword is None) or (keyword is ''):
        return None

    keys=keyword.split()

    if (len(keys)>0 and len(keys)==1):
        from models import searchProduct
        #Column: ID, Brand_id, ProductType_ID, Name
        productResult=searchProduct(keys[0])
        if (productResult is not None and len(productResult)>0):
            #"a.ID, a.Name, a.Website, a.outUrl, a.ProductID, e.color, c.BrandName, g.RetailPrice,g.SalePrice "
            #name, id, brandName, color, retail, sale, weburl):
            for item in productResult:
                try:
                    product=Product(item[1],item[0],item[6],item[5],item[7],item[8],item[3])
                    result=dict(name=product._productName,price=product._price, saleprice=product._saleprice, color=product._color, url=product._webUrl, brand=product._brand, pic_url=product._pic_path)
                    resultList.append(result)
                except:
                    pass

    return resultList




#re=SearchProductByKeyword("Jimmy")
#print re
