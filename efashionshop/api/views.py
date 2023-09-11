from http.client import NOT_FOUND
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from threading import Timer

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from store.models import  Customer, NonRegistredOrder, Order, Product, ProductSet, Review, nonregistredCustomer
from django.shortcuts import render
from .serializers import  CustomerSerializer, NonRegistredCustomerSerializer, OrderSerializer, ProductSerializer,CustomTokenObtainPairSerializer, ReviewSerializer, UserSerializer
from rest_framework import generics
from django.db.models import Q
from rest_framework import filters
from .pagination import CustomPagination
from operator import itemgetter
from django.contrib.auth.models import User
from .utils import validate_password_strength,orderMail,mailToken
from rest_framework import serializers
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,  
    TokenRefreshView,  
)


import re   

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'



def automaticallyDeletingOrder(customer):
    print('automatically deleting')
    print(customer.cart.all())
    print('automatically deleting')
    print(customer.cart)
    for c in customer.cart.all():
        product=c.product
        print('elements')
        #returning quantity to original
        print(product)
        product.quantity=product.quantity+c.quantity
        product.save()
        print(product.quantity)



def generateCart(customer,request):
    cart=request.data['productId']
    quantity=request.data['quantity']
    customer.cart.clear()

    for i in range(len(cart)):
        try:
            product = Product.objects.get(id=cart[i])
            quant=int(quantity[i])
            print(quant)
            product.generateOrder(quantityProd=quant)
            print(product.quantity)
            product.save()
            print(quant)
            try:
                item = ProductSet.objects.distinct().get(
                Q(product=product)
                & Q(quantity=quant)
                )
                print(item)
            except ProductSet.DoesNotExist:
                item=ProductSet(product=product,quantity=quant)
                print(item)    

            item.save()
            customer.save()
            customer.cart.add(item)
                
        except Product.DoesNotExist:
            raise NOT_FOUND()


 


@api_view(['GET'])
def getRoutes(request):
 
    
    routes=[
        {'POST':'url: /api/users/custom-token/ returns: token refresh, token access and isAdmin demands: body data- password and username' },
        {'POST':'url: /api/users/token/refresh/ returns: token access demands: body data- token refresh' },
        {'POST':'url: /api/createNonRegistred/ createsNonRegistredCustomer returns: string if the length of phone number is less  than 10 or email is invalid otherwise nonRegistredCustomer demands: body data: phoneNumber, firstName,lastName, address,email and cart(productId, quantity)' }, 
        {'GET':'url: /api/products/<str:pk>/ get product based on id' },
        {'GET':'url: /api/getProducts/ get products with query params' },
        {'GET':'url: /api/getCustomer/ returns: customer, demands: access token-Auth Bearer' },
        {'DELETE':'url: /api/deleteCart/ deletes customer cart  demands: access token -Auth Bearer' },
        {'PUT':'url: /api/updateCart/ updates customer cart (productId, quantinty) with the limited time period of 30 minutes, demands: access token -Auth Bearer, body data- productId, quantinty' },
        {'PUT':'url: /api/editCustomer/ updates customer, demands:  access token -Auth Bearer customer body data: phoneNumber, firstName,lastName, address returns: string if the length of phone number is less than 10 otherwise it returns edited customer. Note: cart is updated with updateCart' },
        {'POST':'url: /api/createOrder/  creates order for registred customers requires token access returns generated order and sends email to customer with order details' },
        {'POST':'url: /api/orderCreateNonRegistred/  creates order for nonregistred customers requires customer body data: id ,returns generated order and sends email to customer with order details' },
        {'GET':'url: /api/getOrders/ returns: customers orders, demands: access token -Auth Bearer' },
        {'POST':'url: /api/createCustomer/ returns: customer or string if data is invalid , demands: body data: username,email,password, confirm_password' },
        {'GET':'url: /api/uniqueAttributtes/ returns: subcategory and product type pairs' },
        {'POST':'url: /api/productAdd/ demands: admin access token-Auth Bearer and product data inside the body (all product fields), returns: created Product' },
        {'POST':'url: /api/productUpdate/<str:pk>/ demands: admin access token -Auth Bearer and product data inside the body (all product fields) and product id in the url, returns: created Product' },
        {'DELETE':'url: /api/productDelete/<str:pk>/ deletes product  demands: access token -Auth Bearer and product id in the url returns:deleted Product' },
        {'POST':'url: /api/postReview/ demands: admin access token -Auth Bearer and product data inside the body (field product) , returns: created Review' },
        {'GET':'url: /api/review/<str:pk>/ demands: id of product in the url, returns reviews of the product' },
        {'PUT':'url: /api/sendTemporaryToken/ sends temporary token for password change, demands: body data- email' },
        {'PUT':'url: /api/passwordChange/ password change, demands: body data: email,password, confirm_password,token, returns message as string' },

        
        


        


       


        

     
    


    ]
    context={'routes':routes}
  
    return render(request,'api/home.html', context=context)






@api_view(['POST'])
@permission_classes([IsAuthenticated]) #dodala sam 
def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    print('request data')
    print(request.data)
    serializer= ProductSerializer(data=request.data,instance=product)
    print('update product')
    print(serializer.is_valid())
    print(serializer.errors)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    


    




@api_view(['GET'])
def getProduct(request,pk):
    product=get_object_or_404(Product,id=pk)
    serializer=ProductSerializer(product, many=False) #take query set projects and turn into json data many vise objekata
    print(type(serializer.data))
    product_dict={"numberOfStars":product.getNumberOfStars}
    product_dict.update(serializer.data)
    return Response(product_dict)


@api_view(['GET'])
def getReview(request,pk):
    product=get_object_or_404(Product,id=pk)
    print(type(product.getReview))
    print('get reviews')
    print(product.getReview)
    serilazer=ReviewSerializer(product.getReview,many=True)
   
    return Response(serilazer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postReview(request):
    print('post review')
    review = Review()
    data=request.data
    product=get_object_or_404(Product,id=data['product'])
    customer = request.user.customer
    review.product=product
    review.owner=customer
    review.value=int(data['value'])
    review.body=data['body']
    review.setOwnerName()
    review.save()
    
    serilazer=ReviewSerializer(review)
   
    return Response(serilazer.data)






@api_view(['POST'])
def createCustomer(request):
    text="Registration failed. Reason: "
    data=request.data
    print(data['username'])
    print(User.objects.filter(username=data["username"]).exists())

    if(User.objects.filter(username=data["username"]).exists()):
        return Response(text+ "Username exists")
    
    if(User.objects.filter(email=data["email"]).exists()):
        return Response(text+ "User with that email already exists")
    
    if(not re.fullmatch(regex, data["email"])):
        return Response(text+ "Invalid email")
    
    if (validate_password_strength(data["password"]) != "OK"):
        return Response(text+ validate_password_strength(data["password"]))

    
    

    if data["password"] !=data["confirm_password"]:
       return Response(text+ "The two password fields must match.")

        
    user = User.objects.create_user(username=data["username"], password=data["password"], email=data["email"])
    user.save()
    serializer=UserSerializer(user,many=False)
    # customer = Customer.objects.create(
    #     user=user,
    # )
    

    return Response(serializer.data)


@api_view(['PUT'])  #treba patch
def passwordChange(request):
    data=request.data
    text="Password change failed. Reason: "
    if(User.objects.filter(email=data["email"]).exists()):
        user=User.objects.get(email=data["email"])
        customer=Customer.objects.get(user_id=user.id)
        if(customer.temporaryToken !=data['token']):
            return Response(text+ "Token is not valid.")

        if (validate_password_strength(data["password"]) != "OK"):
           return Response(text+ validate_password_strength(data["password"]))

        if data["password"] !=data["confirm_password"]:
           return Response(text+ "The two password fields must match.")
        
        user.password=data["password"]

        return Response('Password changed successfully!')
    
    return Response("User with that email doesnt exist")





@api_view(['PUT'])  #treba patch
def sendTemporaryToken(request):

    data=request.data
    if(User.objects.filter(email=data["email"]).exists()):
        user=User.objects.get(email=data["email"])
        if(Customer.objects.filter(user=user).exists()):
            email=data["email"]
            customer=Customer.objects.get(user_id=user.id)

        else:
            return Response("User with that email doesnt exist")
    
    mailToken(email,customer)
   
   
    
    return Response('Token was sent on your email adress')


@api_view(['POST'])  #treba patch
@permission_classes([IsAuthenticated])
def createOrder(request):
    customer = request.user.customer
    customerEmail=request.user.email
    newOrder=Order()
    newOrder.customer=customer
    newOrder.status=True
    newOrder.save()
    newOrder.placeOrder()
    data={'order':newOrder}
    orderMail(data,customerEmail)
    
    
    #newOrder.save()
    return Response('order created')





@api_view(['POST'])
def createNonRegistredOrder(request):
    print('create non registred order')
    pk=request.data['id']
    print(pk)
    customer=get_object_or_404(nonregistredCustomer,id=pk)
    print(customer)
    customerEmail=customer.email
    print(customerEmail)
    newOrder=NonRegistredOrder()
    newOrder.nonRegCustomer=customer
    newOrder.status=True
    newOrder.save()
    newOrder.placeOrder()
 
    data={'order':newOrder}
    orderMail(data,customerEmail)
   
    
    return Response('order created')
    


@api_view(['POST'])  
def createNonRegistredCustomer(request):
    #moze da ima isti mail
    data=request.data
    print(data)
    customer=nonregistredCustomer()

    data=request.data
    customer.fullName=data['firstName']+' '+ data['lastName']
    customer.address=data['address']
    customer.email=data['email']
    customer.phoneNumber=data['phoneNumber']


    if len(str(data['phoneNumber'])) !=10:
        return Response('Phone number must contain 10 digits')
    
    if(not re.fullmatch(regex, data["email"])):
        return Response("Invalid email")
    
    # i ovde kada kreiram neregistrovanog
    generateCart(customer,request)   
    

    
    serializer=NonRegistredCustomerSerializer(customer, many=False) #take query set projects and turn into json data many vise objekata
    return Response(serializer.data)


@api_view(['PUT'])  #treba patch
@permission_classes([IsAuthenticated])
def editCustomer(request):
    customer = request.user.customer
    print(request.data)
    data=request.data
    customer.fullName=data['firstName']+' '+ data['lastName']
    customer.address=data['address']
    if len(str(data['phoneNumber'])) !=10:
        return Response('Phone number must contain 10 digits')
    

    customer.phoneNumber=data['phoneNumber']
    customer.save()

    
    serializer=CustomerSerializer(customer, many=False) 
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCustomer(request):
    customer = request.user.customer
    serializer=CustomerSerializer(customer, many=False) 
    print(serializer.data)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrdersbyCustomer(request):
    customer = request.user.customer
    order=Order().get_orders_by_customer(customer_id=customer.id)
    serializer=OrderSerializer(order,many=True)

    return Response(serializer.data)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCart(request):
    customer = request.user.customer
    customer.cart.clear()
    return Response("cart deleted!")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCart(request): 
    #saving cart for 30 minutes
    customer = request.user.customer
    generateCart(customer,request)
    print(type(customer))
    t = Timer(1800, automaticallyDeletingOrder,args=(customer,))
    t.start()
   
    return Response("cart saved!")


    
    




@api_view(['POST'])
@permission_classes([IsAuthenticated])

def createProduct(request):

    data=request.data
    print('request data')
    print(data)
    product = ProductSerializer(data=data)
    print(product)
    try:
        existingProduct=Product.objects.get(productTitle__contains=data['productTitle'])
        return ValidationError('product with that title  already exists'+ 'title: '+ existingProduct.productTitle)
    except:
        print(product.is_valid())
    
        if product.is_valid():
            product.save()
            productSaved=Product.objects.get(productTitle=data['productTitle'])
            productSaved.generateSimiliar()
            return Response(product.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
@api_view(['GET'])
def getSubCategoryProductTypePair(request):
    products=Product.objects.all()
    listProduct=list(products)
    subCategory= [o.subCategory for o in listProduct]
    productType= [o.productType for o in listProduct]
    sub_un=list(set(subCategory))
    new_dict={}
    for sub in sub_un:
        indexes=[i for i, j in enumerate(subCategory) if j == sub]
        new_dict[sub.replace(' ', '_')]=list(set(itemgetter(*indexes)(productType)))
    print(new_dict)
        
    
    return Response(new_dict)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProduct(request,pk):
    print('deleting')
    product=get_object_or_404(Product,id=pk)
    product.delete()
    serializer=ProductSerializer(product, many=False) #take query set projects and turn into json data many vise objekata
    return Response(serializer.data)




class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer




class ProductsDataView(generics.ListAPIView):
    #get products based on params: search, filter, pagination and chosed fields
    serializer_class= ProductSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ['category', 'colour', 'gender', 'productTitle', 
     'productType', 'subCategory', 'usage']
    pagination_class = CustomPagination
    def get_queryset(self):
           if self.request.method == 'GET':
            queryset = Product.objects.all()
            gender = self.request.GET.get('gender', '')
            category = self.request.GET.get('category', '')
            subCategory = self.request.GET.get('subCategory', '')
            productType = self.request.GET.get('productType', '')
            colour = self.request.GET.get('colour', '')
            usage = self.request.GET.get('usage', '')
            productTitle = self.request.GET.get('productTitle', '')
            queryGender=Q(gender=gender)
            if (gender==''):
                queryGender=Q(gender__contains=gender)
           

           
            queryset = Product.objects.distinct().filter(
              queryGender
             & Q(category__contains=category)
             & Q(colour__contains=colour.capitalize())
             & Q(subCategory__contains=subCategory.capitalize())
             & Q(productType__contains=productType.capitalize())
             & Q(usage__contains=usage.capitalize())
             & Q(productTitle__contains=productTitle.capitalize())
             )
            
           
            
             
            return queryset
           
          
   

          
          
            
    
          
        






