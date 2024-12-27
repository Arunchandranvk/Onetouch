from django.urls  import path
from .views import *

urlpatterns = [
        #common
        path('login/',LoginView.as_view(),name='log'),
        path('product/<int:pk>/',ProductGetView.as_view(),name='product'),
        path('product-all/',AllProductsView.as_view(),name='all-product'),
        path('category-all/',AllCategoryView.as_view(),name='all-category'),
        path('category-update/<int:pk>/',CategoryUpdateView.as_view(),name='category-update'),

        #User
        path('registration/',RegistrationStudentView.as_view(),name='reg'),
        path('profile/',ProfileView.as_view(),name='profile'),
        path('profile-update/<int:pk>/',ProfileUpdateView.as_view(),name='update_profile'),
        path('get_category_itemlist/<int:pk>/',CateogoryProductListView.as_view(),name='cat_list'),
        path('appointment-create/',AppoinmentCreateView.as_view(),name='app-create'),
        path('appointment-user/',AppointmentsUserView.as_view(),name='app-user'),
        path('cart/',CartItemCreateView.as_view(),name='cart-add'),
        path('cart-all/',CartItemListView.as_view(),name='cart-my'),
        path('cart-quantity-update/<int:pk>/',CartProductQuantityUpdateView.as_view(),name='cart-quantity'),
        path('cart-item-delete/<int:pk>/',CartItemDeleteView.as_view(),name='cart-item-delete'),
        path('cart-checkout/',cart_checkout,name='checkout-cart'),
        path('checkout/<int:product_id>/',Direct_checkout,name='checkout'),
        path('my-orders/',my_orders,name='myorders'),
        path('cart-status/<int:product_id>/',product_in_cart,name='cart-status'),
        
        #Admin
        path('product-create/',ProductCreateView.as_view(),name='product_add'),
        path('product-update/<int:pk>/',ProductUpdateView.as_view(),name='product_update'),
        path('product-delete/<int:pk>/',ProductDeleteView.as_view(),name='product_delete'),
        path('category-create/',CategoryCreateView.as_view(),name='cat_create'),
        path('appointment-all/',AllAppointmentsView.as_view(),name='app-all'),
        path('appointment-status-Update/<int:pk>/',AppontmentStatusUpdateView.as_view(),name='app-status-up'),
        path('all-orders/',AllOrders,name='all-order'),
        path('update-order-status/<int:order_id>/',update_order_status,name='ordr-status')
    ]