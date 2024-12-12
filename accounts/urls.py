from django.urls  import path
from .views import *

urlpatterns = [
        #common
        path('login',LoginView.as_view(),name='log'),
        path('product/<int:pk>/',ProductGetView.as_view(),name='product'),
        path('product-all/',AllProductsView.as_view(),name='all'),

        #User

        path('registration/',RegistrationStudentView.as_view(),name='reg'),
        path('profile/',ProfileView.as_view(),name='profile'),
        path('profile-update/<int:pk>/',ProfileUpdateView.as_view(),name='update_profile'),

        

        #Admin
        path('product-create/',ProductCreateView.as_view(),name='product_add'),
        path('product-update/<int:pk>/',ProductUpdateView.as_view(),name='product_update'),
        path('product-delete/<int:pk>/',ProductDeleteView.as_view(),name='product_delete'),
        path('category-create/',CategoryCreateView.as_view(),name='cat_create'),

        

    ]