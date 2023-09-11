from rest_framework import serializers
from store.models import  NonRegistredOrder, Product,Customer,Order,Admin, ProductSet, Review, nonregistredCustomer #nije bio ni dostupan child
from django.contrib.auth.models import User
#will convert project object into json object
#pogledaj project model




class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email']



# class CartSerializer(serializers.ModelSerializer):
#     carts=ProductSerializer(many=True,read_only=True)
#     #items = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
#     class Meta:
#         model=Cart
#         fields='__all__'
        
    # def create(self, validated_data):
    #     print(validated_data)
    #     tracks_data = validated_data.pop('cart')
    #     album = Product.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Cart.objects.create(album=album, **track_data)
    #     return album
    

class ProductSerializer(serializers.ModelSerializer):
    #cart_list = CartSerializer(many=True, read_only=True)
    #id = serializers.IntegerField()
    class Meta:
        model=Product
        fields='__all__'

class ProductSetSerializer(serializers.ModelSerializer):
    #cart_list = CartSerializer(many=True, read_only=True)
    #id = serializers.IntegerField()
    class Meta:
        model=ProductSet
        fields='__all__'


class ReviewSerializer(serializers.ModelSerializer):
    #cart_list = CartSerializer(many=True, read_only=True)
    #id = serializers.IntegerField()
    class Meta:
        model=Review
        fields='__all__'


    

class CustomerSerializer(serializers.ModelSerializer):
    cart= ProductSetSerializer(many=True, read_only=True)
    class Meta:
        model=Customer
        fields='__all__'
        #extra_kwargs = {'itemsCart': {'required': False}}

    # def create(self, validated_data):
    #     cart_data= validated_data.pop('cart')
    #     #if customer exists
    #     customer = Customer.objects.create(**validated_data)
    #     for cart_data in cart_data:
    #         Customer.objects.create(customer=customer, **cart_data)
    #     return customer



        #extra_kwargs = {'carts': {'required': False}}

class NonRegistredCustomerSerializer(serializers.ModelSerializer):
    cart= ProductSetSerializer(many=True, read_only=True)
    class Meta:
        model=nonregistredCustomer
        fields='__all__'



class OrderSerializer(serializers.ModelSerializer):
    cart= ProductSetSerializer(many=True, read_only=True)
    class Meta:
        model=Order
        fields='__all__'


class NonRegistredOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=NonRegistredOrder
        fields='__all__'


#https://stackoverflow.com/questions/53480770/how-to-return-custom-data-with-access-and-refresh-tokens-to-identify-users-in-dj
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # with token access and refresh returns if logged user is a admin 
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'admin':False})
        isAdmin=Admin.objects.filter(user=self.user)
        print(isAdmin)
        if (isAdmin):
             data.update({'admin':True})
       
        return data
    

