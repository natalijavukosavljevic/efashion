
from django.db.models.signals import post_save, post_delete
from .models import Customer,Admin
from django.contrib.auth.models import User 


def createCustomer(sender, instance, created, **kwargs):
    if created:
        user = instance
        customer = Customer.objects.create(
            user=user,
        )

def createAdmin(sender, instance, created, **kwargs):
    if created:
        user = instance
        admin = Admin.objects.create(
            user=user,
        )



def updateUser(sender, instance, created, **kwargs):
    customer = instance
    user= customer.user 
    if created==False:
        user.save() 



def deleteUser(sender, instance, **kwargs): 
    print("Deleting user...")
    try:
        user=instance.user
        user.delete()
    except:
        pass

post_save.connect(createCustomer,sender=User) 

post_save.connect(updateUser,sender=Customer) 

post_delete.connect(deleteUser,sender=Customer)  

post_save.connect(updateUser,sender=Admin)
post_delete.connect(deleteUser,sender=Admin)