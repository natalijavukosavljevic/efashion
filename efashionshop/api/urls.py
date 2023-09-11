from django.urls import path,include
#create static for our url file
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  #gemerise token za usera token koji traje 5 minuta da ga ne bi niko ukrao
    TokenRefreshView,  # generise token koji traje 30 dana
)

from . import views
urlpatterns=[
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/custom-token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('',views.getRoutes), 
    path('products/<str:pk>/', views.getProduct), 
    path('productAdd/', views.createProduct),
    path('productDelete/<str:pk>/', views.deleteProduct),
    path('getProducts/',views.ProductsDataView.as_view()),
    path('productUpdate/<str:pk>/', views.update_product),
    path('uniqueAttributtes/',views.getSubCategoryProductTypePair),
    path('createCustomer/',views.createCustomer),
    path('getCustomer/', views.getCustomer),
    path('editCustomer/', views.editCustomer),
    path('updateCart/', views.updateCart),
    path('deleteCart/', views.deleteCart),
    path('createNonRegistred/',views.createNonRegistredCustomer),
    path('orderCreateNonRegistred/',views.createNonRegistredOrder), 
    path('createOrder/',views.createOrder),
    path('getOrders/',views.getOrdersbyCustomer),
    path('sendTemporaryToken/',views.sendTemporaryToken),
    path('passwordChange/',views.passwordChange),
    path('review/<str:pk>/', views.getReview), 
    path('postReview/', views.postReview), 
    
    
    
    

] 
