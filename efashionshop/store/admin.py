from django.contrib import admin

from .models import Product,Customer,Order,Admin,ProductSet, Review,nonregistredCustomer,NonRegistredOrder
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Admin)
admin.site.register(ProductSet)
admin.site.register(nonregistredCustomer)
admin.site.register(NonRegistredOrder)
admin.site.register(Review)

# Register your models here.
