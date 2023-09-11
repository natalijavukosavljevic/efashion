import operator
from store.models import Product
import csv
from PIL import Image
from django.core.files.base import ContentFile


from store.models import Product
# import random
# for item in Product.objects.all():
#     item.quantity=random.randint(5,50)
#     item.price=random.randint(5,100)
#     item.save()


productTitles=[]
images=[]

def run():
    for item in Product.objects.all():
        # binarySim=''
        # #genderList=Product.objects.values_list('gender', flat=True).distinct()
        # def binaryRep(index,fieldList,binarySim):
        #     for i in range(len(fieldList)):
        #         if (i==index):
        #             binarySim+='1'
        #         else:
        #             binarySim+='0'
        #     return binarySim
        # fieldList=list(Product.objects.values_list('gender', flat=True).distinct())
        # index=fieldList.index(item.gender)
        # binarySim=binaryRep(index,fieldList,binarySim)
        # fieldList=list(Product.objects.values_list('productType', flat=True).distinct())
        # index=fieldList.index(item.productType)
        # binarySim=binaryRep(index,fieldList,binarySim)
        # fieldList=list(Product.objects.values_list('subCategory', flat=True).distinct())
        # index=fieldList.index(item.subCategory)
        # binarySim=binaryRep(index,fieldList,binarySim)
        # fieldList=list(Product.objects.values_list('category', flat=True).distinct())
        # index=fieldList.index(item.category)
        # binarySim=binaryRep(index,fieldList,binarySim)
        # fieldList=list(Product.objects.values_list('colour', flat=True).distinct())
        # index=fieldList.index(item.colour)
        # binarySim=binaryRep(index,fieldList,binarySim)
        # fieldList=list(Product.objects.values_list('usage', flat=True).distinct())
        # index=fieldList.index(item.usage)
        # binarySim=binaryRep(index,fieldList,binarySim)
        # item.binarySim=binarySim
        # item.save()
        #item=Product.objects.get(id=32840)
        productsList=Product.objects.filter(gender=item.gender)
        # Converting String to binary
        temp=int(item.binarySim, 2)
        diffrence=[]
        indices=[]

        for product in productsList:
            diffrence.append(abs(temp-int(product.binarySim,2)))
            indices.append(product.id)

        data = sorted(enumerate(diffrence), key=operator.itemgetter(1))[:6]
        newlist = [x[0] for x in data]
        print(data)
        print(newlist)
        print((operator.itemgetter(*newlist)(indices)))
        tempTuple=(operator.itemgetter(*newlist)(indices))
        listTempTuple=list(tempTuple)
        print(listTempTuple)
        if item.id in listTempTuple:
            listTempTuple.remove(item.id)
        else:
            listTempTuple.pop()
        print(listTempTuple)
        tempTupleStr=",".join(map(str,tuple(listTempTuple)))
        print(tempTupleStr)
        item.mostSimilar=tempTupleStr
        item.save()
        


        

        #for gender in gender
        #


            
            #'D:/nata/archive/data/allImages/'+ row[8]
            #with open('D:/nata/archive/data/allImages/'+ row[8], errors="ignore") as f:
            #     data = f.read()
            # image = Image.open("image_path.jpg")
            # product.productImage.save(row[8], image)
        