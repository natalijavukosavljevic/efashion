import math
import operator
import random
from django.db import models
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import AbstractUser
import datetime
import uuid
from django.contrib.auth.models import User
from urllib import request
import os
from PIL import Image
from PIL import ImageChops
from django.forms import ValidationError


def generateTokenPasswordChange():
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

    ## initializing a string
    random_str = ""
    ## we can generate any lenght of string we want
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str

def binaryRep(index,fieldList,binarySim):
    for i in range(len(fieldList)):
        if (i==index):
            binarySim+='1'
        else:
            binarySim+='0'
    return binarySim


def generationBinary(item):
    binarySim=''
    fieldList=list(Product.objects.values_list('gender', flat=True).distinct())
    index=fieldList.index(item.gender)
    binarySim=binaryRep(index,fieldList,binarySim)
    fieldList=list(Product.objects.values_list('productType', flat=True).distinct())
    index=fieldList.index(item.productType)
    binarySim=binaryRep(index,fieldList,binarySim)
    fieldList=list(Product.objects.values_list('subCategory', flat=True).distinct())
    index=fieldList.index(item.subCategory)
    binarySim=binaryRep(index,fieldList,binarySim)
    fieldList=list(Product.objects.values_list('category', flat=True).distinct())
    index=fieldList.index(item.category)
    binarySim=binaryRep(index,fieldList,binarySim)
    fieldList=list(Product.objects.values_list('colour', flat=True).distinct())
    index=fieldList.index(item.colour)
    binarySim=binaryRep(index,fieldList,binarySim)
    fieldList=list(Product.objects.values_list('usage', flat=True).distinct())
    index=fieldList.index(item.usage)
    binarySim=binaryRep(index,fieldList,binarySim)
    item.binarySim=binarySim
    item.save()

def generateSimiliarProducts(item):
    temp=int(item.binarySim, 2)
    productsList=Product.objects.filter(gender=item.gender)
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




# Create your models here.

class Product(models.Model):
    #dodati atribut za ordering



    GENDER_CHOICES = (
    ("boys", "boys"),
    ("girls", "girls"),
    ("men", "men"),
    ("women", "women"),
    )
    

    CATEGORY_CHOICES=(
        ("footwear","footwear"),
        ("apparel","apparel")
    )

    subCategory = models.CharField(max_length=200, null=True, blank=True)
    productType=models.CharField(max_length=200, null=True, blank=True)
    quantity=models.IntegerField(null=True,blank=True, default=1)
    price=models.FloatField(null=True,blank=True, default=1)

    gender = models.CharField(
        max_length = 20,
        choices = GENDER_CHOICES,
        default = 'boys'
        )
    
    category = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        default = 'apparel'
        )
    colour = models.CharField(max_length=200, null=True, blank=True)
    usage= models.CharField(max_length=400, null=True, blank=True)
    productTitle=models.CharField(max_length=200, null=True, blank=True)
    
    productImage= models.ImageField(null=True, blank=True, upload_to="products/", default="products/default.jpg") #da bi ovo koristili moramli smo pillow instalirati
    id = models.AutoField(primary_key=True)
    imageUrl=models.CharField(max_length=1000, null=True, blank=True)
    binarySim=models.CharField(max_length=200, null=True, blank=True)
    mostSimilar=models.CharField(max_length=100, null=True, blank=True)
   

    class Meta:
        ordering=['-gender']


   

    def get_remote_image(self,images):
        duplicate=False
        if self.imageUrl :
            result = request.urlretrieve(self.imageUrl)
            im = Image.open(result[0])
            for imc in images:
                diff = ImageChops.difference(im, imc)
                if diff.getbbox():
                    print("images diffrent")
                else:
                    print ("same")
                    duplicate=True
                    return duplicate
               
           
            images.append(im)
            self.productImage.save(
                    os.path.basename(str(self.id)+'.jpg'),
                    File(open(result[0], 'rb'))
                    )
            duplicate=False
            return duplicate
        
    def generateOrder(self,quantityProd=1):
       
        if self.quantity-quantityProd>=0:
            self.quantity=self.quantity-quantityProd
        else:
            raise ValidationError( self.productTitle+ ' is no longer available')

    def generateSimiliar(self):
        generationBinary(self)
        generateSimiliarProducts(self)

        

    @property
    def getReview(self):
        reviews = self.review_set.all()
        return reviews
    
    @property
    def getNumberOfStars(self):
        reviews = self.review_set.all()
        suma=0
        for review in reviews:
            suma+=review.value

        #votes= reviews.value.count()
        totalVotes=reviews.count()
        if (totalVotes>0):
           numberOfStars=suma/totalVotes
        else:
            numberOfStars=0

        return numberOfStars
    
 

        
                    
             
        


class Admin(models.Model):
    #access='FlURhDve0nJwrAG'
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class ProductSet(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE)   
    def __str__(self):
        return str(self.quantity) + " " +self.product.productTitle


class Customer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullName=models.CharField(max_length=50, default='', blank=True)
    phoneNumber = models.CharField(max_length=10,null=True, blank=True)
    address = models.CharField(max_length=50, default='', blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    temporaryToken=models.CharField(max_length=6, default='', blank=True)
    cart = models.ManyToManyField(
        'ProductSet',
        blank=True
    )
    def __str__(self):
       return self.fullName+  ' ' +self.user.username
    
    def generateTemporaryToken(self):
        self.temporaryToken=generateTokenPasswordChange()
        self.save()
        return self.temporaryToken
    
    

        
    #related_name='carts',


class nonregistredCustomer(models.Model):
    fullName=models.CharField(max_length=50, default='', blank=True)
    email=models.CharField(max_length=50, default='', blank=True)
    phoneNumber = models.CharField(max_length=10,null=True, blank=True)
    address = models.CharField(max_length=50, default='', blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    cart = models.ManyToManyField(
        'ProductSet',
        blank=True
    )
    def __str__(self):
       return self.fullName


class NonRegistredOrder(models.Model):
   
    nonRegCustomer = models.ForeignKey(nonregistredCustomer,
                                 on_delete=models.CASCADE)
    
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    address = models.CharField(max_length=50, default='', blank=True)
    phoneNumber = models.CharField(max_length=10,null=True, blank=True)
    price= models.FloatField(blank=True, default=0)

    cart = models.ManyToManyField(
        'ProductSet',
        blank=True
    )

  
    def placeOrder(self):
        print('in place order')
        print(self.nonRegCustomer)
        priceTemp=0
        cartNonCustomer=self.nonRegCustomer.cart.all()
        print(cartNonCustomer)
        for c in cartNonCustomer:
            priceTemp+=c.product.price*c.quantity

        self.price=priceTemp
        self.address=self.nonRegCustomer.address
        self.phoneNumber=self.nonRegCustomer.phoneNumber
        self.status=True
        print(self.status)
        print(cartNonCustomer)
       #IntegrityError: FOREIGN KEY constraint failed treba order sacuvati pre nego sto se refenciras na njega
        self.cart.add(*cartNonCustomer)
        self.save()
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')






class Order(models.Model):

    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    
    address = models.CharField(max_length=50, default='', blank=True)
    phoneNumber = models.CharField(max_length=10,null=True, blank=True)
    
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    price= models.FloatField(blank=True, default=0)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    cart = models.ManyToManyField(
        'ProductSet',
        blank=True
    )
  
    def placeOrder(self):
        print('place order')
        print(self.customer)
        priceTemp=0
        cartCustomer=self.customer.cart.all()
        print(cartCustomer)
        for c in cartCustomer:
            priceTemp+=c.product.price*c.quantity

        self.price=priceTemp
        self.address=self.customer.address
        self.phoneNumber=self.customer.phoneNumber
        self.status=True
        print(cartCustomer)
        self.cart.add(*cartCustomer)
        self.save()
  
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    

class Review(models.Model):
    #owner
    #Foreignkey one to many
    ownerName=models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)  
    product= models.ForeignKey(Product, on_delete=models.CASCADE) 
    value=models.IntegerField(null=True,blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 



    #one review per project jedan owner jedan project
    class Meta:
        unique_together=[['owner', 'product']]

    def setOwnerName(self):
        self.ownerName=self.owner.user.username

    def __str__(self):
        return str(self.value)
  