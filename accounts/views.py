from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,parsers
import random
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

class RegistrationStudentView(APIView):
    @swagger_auto_schema(
        request_body=Registration,    
        responses={
            200:openapi.Response('Registration Successfull....',Registration),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        try:
            ser=Registration(data=request.data)
            if ser.is_valid():    
                user = ser.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response(data={"Status": "Success", "Msg": "Registration Successful!!!!", "data": ser.data,"tokens": {
                            "access": access_token,
                            "refresh": refresh_token
                        }}, status=status.HTTP_200_OK)
            else:
                return Response(data={"Status":"Failed","Msg":"Registration Unsuccessfull....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
   
   
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            user_id=request.user.id
            print("user",user_id)
            profile=CustomUser.objects.get(id=user_id)
            print(profile)
            ser=ProfileSer(profile)
            return Response(data={"Status":"Success","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=ProfileSer,    
        responses={
            200:openapi.Response('Profile Updated....',ProfileSer),
            400: 'Validation errors'
        }
    )
    def put(self,request,**kwargs):
        profile_id= kwargs.get('pk')
        try:
            profile=CustomUser.objects.get(id=profile_id)
            ser=ProfileSer(profile,data=request.data,partial=True) 
            if ser.is_valid():
                ser.save()  
                return Response(data={"Status":"Success","Msg":"Profile updated successfully","data": ser.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(
                data={"Status": "Failed", "Msg": "Profile not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            200:openapi.Response('Category Added....',CategorySerializer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=CategorySerializer(data=request.data,context={'request': request})
        if ser.is_valid():    
            ser.save()
            return Response(data={"Status": "Success", "Msg": "Category Added!!!!", "data": ser.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Status":"Failed","Msg":"Something went wrong....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
   
class AllCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            category=Categories.objects.all()
            cat=ProductSer(category,many=True)
            return Response(data={"Status":"Success","Msg": "All Categories","data":cat.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=ProductSer,
        responses={
            200:openapi.Response('Product Added....',ProductSer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=ProductSer(data=request.data,context={'request': request})
        # print(ser)
        if ser.is_valid():    
            ser.save()
            return Response(data={"Status": "Success", "Msg": "Product Added!!!!", "data": ser.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Status":"Failed","Msg":"Something went wrong....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
   
   
class ProductGetView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request,**kwargs):
        try:
            id=kwargs.get('pk')
            products=Products.objects.get(id=id)
            pro=ProductSer(products)
            return Response(data={"Status":"Success","data":pro.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=ProductSer,    
        responses={
            200:openapi.Response('Product Updated....',ProductSer),
            400: 'Validation errors'
        })
    def put(self,request,**kwargs):
        product_id= kwargs.get('pk')
        try:
            product=Products.objects.get(id=product_id)
            print(request.user)
            ser=ProductSer(product,data=request.data,partial=True) 
            if ser.is_valid():
                ser.save()  
                return Response(data={"Status":"Success","Msg":"Product updated successfully","data": ser.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except Products.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Product not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def delete(self,request,**kwargs):
        try:
            product_id=kwargs.get('pk')
            product=Products.objects.get(id=product_id)
            product.delete()
            return Response({"Status":"Success","Msg":f"{product.product_name} Deleted Successfully!!!!!"})
        except Exception as e:
            return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllProductsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            products=Products.objects.all()
            pro=ProductSer(products,many=True)
            return Response(data={"Status":"Success","Msg": "All Products","data":pro.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        

class CateogoryProductListView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request,**kwargs):
        try:
            category_id=kwargs.get('pk')
            cat=Categories.objects.get(id=category_id)
            products=Products.objects.filter(category_name=category_id)
            ser=ProductSer(products,many=True)
            return Response(data={"Status":"Success","Msg":f"Products listed in {cat.category_name} Category","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)
        

class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=CategorySerializer,    
        responses={
            200:openapi.Response('Category Updated....',CategorySerializer),
            400: 'Validation errors'
        })
    def put(self,request,**kwargs):
        try:
            category_id=kwargs.get('pk')
            cat=Categories.objects.get(id=category_id)
            ser=CategorySerializer(cat,data=request.data,partial=True)
            if ser.is_valid():
                ser.save()  
                return Response(data={"Status":"Success","Msg":f"Category  updated successfully","data": ser.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except Categories.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Category not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AppoinmentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=AppoinmentSerializer,
        responses={
            200:openapi.Response('Appointment Added....',AppoinmentSerializer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        try:
            ser=AppoinmentSerializer(data=request.data)
            if ser.is_valid():    
                ser.save()
                return Response(data={"Status": "Success", "Msg": "Appointment Added!!!!", "data": ser.data}, status=status.HTTP_200_OK)
            else:
                return Response(data={"Status":"Failed","Msg":"Something went wrong....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        


class AppointmentsUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):  
        try:
            user=request.user.id
            print(user)
            app=Appoinment.objects.filter(user_id=user)
            ser=AppoinmentSerializer(app,many=True)
            return Response(data={"Status":"Success","Msg": "User Appointments","data":ser.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        

class AllAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):  
        try:
            app=Appoinment.objects.all()
            ser=AppoinmentSerializer(app,many=True)
            return Response(data={"Status":"Success","Msg": "All Appointments","data":ser.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        

class AppontmentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=AppoinmentStatusSerializer,    
        responses={
            200:openapi.Response('Appointment Status Updated....',AppoinmentStatusSerializer),
            400: 'Validation errors'
        })
    def put(self,request,**kwargs):
        try:
            app_id=kwargs.get('pk')
            app=Appoinment.objects.get(id=app_id)
            ser=AppoinmentStatusSerializer(app,data=request.data,partial=True)
            if ser.is_valid():
                ser.save()  
                return Response(data={"Status":"Success","Msg":f"Appointment Status  updated successfully","data": ser.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except Categories.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Appointment not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CartItemCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=CartItemSerializer,    
        responses={
            200:openapi.Response('Cart Item Added....',CartItemSerializer),
            400: 'Validation errors'
        })
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        print(product_id)
        quantity = request.data.get('quantity')
        print(quantity)
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        if quantity > product.stock:
            return Response({'detail': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)
        if quantity < 1:
            return Response({'detail':'Quantity must be at least 1.'})
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart.total_amount += Decimal(product.offer_price) * quantity
        print(product.offer_price * quantity)
        total=cart.total_amount
        print("Total amount",total)
        tax = round(total * Decimal("0.025"), 2)
        total_with_tax = round(total + tax, 2)
        cart.tax=tax
        cart.total_payable=total_with_tax
        cart_item.cart=cart
        cart_item.quantity=quantity
        cart_item.save()
        cart.save()
        ser=CartItemSerializer(cart_item)
        return Response(data={"Status":"Success","Msg":"Product added to cart","data":ser.data}, status=status.HTTP_201_CREATED)

from decimal import Decimal
import random

class CartItemListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            return Response({"detail":"No Items!!"},status=status.HTTP_200_OK)
        
        cart.save()
        if not cart:
            return Response({'detail': 'No active items found'}, status=status.HTTP_200_OK)
        serializer = CartItemSer(cart.items.all(), many=True)
        return Response(data={"Status":"Success","Msg":"My Cart Items","data":serializer.data,'Total Amount':cart.total_amount,'tax':cart.tax,'payable':cart.total_payable},status=status.HTTP_200_OK)
    

class CartProductQuantityUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=CartItemQuantitySer,    
        responses={
            200:openapi.Response('Cart Product Quantity  Updated....',CartItemQuantitySer),
            400: 'Validation errors'
        })
    def put(self,request,**kwargs):
        try:
            cartitem_id=kwargs.get('pk')
            cartitem=CartItem.objects.get(id=cartitem_id)
            new_quantity = request.data.get('quantity')
            product = cartitem.product
            if new_quantity > product.stock:
                return Response(
                    data={"Status": "Failed", "Msg": "Not enough stock available."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ser=CartItemQuantitySer(cartitem,data=request.data,partial=True)
            if ser.is_valid():
                ser.save()  
                serializer=CartItemSer(cartitem)
                cartitem.cart.total_amount = sum(item.total_price for item in cartitem.cart.items.all())
                cartitem.cart.save()

                return Response(data={"Status":"Success","Msg":f"Product Quantity  updated successfully","data": serializer.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except Categories.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Appointment not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Cart Item Deleted'),
            404: 'Cart Item not found',
            400: 'Bad Request'
        })
    def delete(self, request, **kwargs):
        try:
            cartitem_id = kwargs.get('pk')
            cartitem = CartItem.objects.get(id=cartitem_id)
            if cartitem.cart.user != request.user:
                return Response({"Status": "Failed", "Msg": "You do not have permission to delete this item."},
                                status=status.HTTP_403_FORBIDDEN)
            cartitem.delete()
            cartitem.cart.total_amount = sum(item.total_price for item in cartitem.cart.items.all())
            cartitem.cart.save()

            return Response(data={"Status": "Success", "Msg": "Cart Item deleted successfully"},
                            status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Cart Item not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.decorators import api_view,authentication_classes,permission_classes


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="Checkout the user's cart and create an order.",
    request_body=OrderSerializer,
    responses={
        201: OrderSerializer,
        400: "Bad Request - Shipping address is required.",
        200: "Cart is empty.",
    }
)
def cart_checkout(request):
    
    user = request.user

    # Get user's cart
    try:
        cart = Cart.objects.get(user=user)
    # cartitem=CartItem.objects.get()
    except:
        return Response({"detail": "Cart is empty."}, status=status.HTTP_200_OK)

    # Get shipping address from the request
    shipping_address = request.data.get('shipping_address')

    if not shipping_address:
        return Response({"detail": "Shipping address is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the order
    order = Order.objects.create(
        user=user,
        shipping_address=shipping_address,
        total_amount=cart.total_amount,
        tax=cart.tax,
        total_payable=cart.total_payable
    )

    # total_amount = 0
    for cart_item in cart.items.all():
        cart_item.product.stock-=cart_item.quantity
        cart_item.product.save()
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.offer_price * cart_item.quantity
        )

    cart.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def Direct_checkout(request, product_id):
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    shipping_address = request.data.get('shipping_address')
    quantity = request.data.get('quantity', 1)  # Default to 1 if no quantity is provided

    if not shipping_address:
        return Response({"detail": "Shipping address is required."}, status=status.HTTP_400_BAD_REQUEST)

    if int(quantity) <= 0:
        return Response({"detail": "Quantity must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate the total price based on quantity
    total_amount = product.offer_price * int(quantity)
    tax_amount = round(total_amount * 0.025, 2)
    payable=total_amount+tax_amount
    # Create the order
    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        total_amount=total_amount,
        tax= tax_amount,
        total_payable = payable,
        
    )

    # Create the order item
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        price=product.offer_price * int(quantity),
    )

    # Return the created order data
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    """
    API to retrieve all orders of the logged-in user.
    """
    try:
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-order_date')
        
        # Serialize the orders
        serializer = OrderSerializer(orders, many=True)
        
        return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllOrders(request):
    """
    API to retrieve all orders .
    """
    try:
        orders = Order.objects.all().order_by('-order_date')
        serializer = OrderSer(orders, many=True)
        
        return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def update_order_status(request, order_id):
    """
    API to update the status of an order.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    new_status = request.data.get('status')
    if new_status not in ['pending', 'completed']:
        return Response(
            {"detail": "Invalid status. Allowed values: 'pending', 'completed'."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    order.status = new_status
    order.save()

    # Return the updated order
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_in_cart(request, product_id):
    """
    API to check if a product is in the user's cart.
    """
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({"is_in_cart": False}, status=status.HTTP_200_OK)

    # Attempt to get the cart item
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        return Response({
            "is_in_cart": True,
            "cartitem_id": cart_item.id,
            "quantity": cart_item.quantity,
        }, status=status.HTTP_200_OK)

    return Response({"is_in_cart": False}, status=status.HTTP_200_OK)



class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Order Canceled'),
            404: 'Order not found',
            400: 'Bad Request'
        })
    def delete(self, request, **kwargs):
        try:
            Order_id = kwargs.get('pk')
            order = Order.objects.get(id=Order_id)
            if order.user != request.user:
                return Response({"Status": "Failed", "Msg": "You do not have permission to cancel this item."},
                                status=status.HTTP_403_FORBIDDEN)
            if order.status == 'completed':
                return Response({"Status": "Failed", "Msg": "Order Completed."},
                                status=status.HTTP_403_FORBIDDEN)
            order.delete()
            # cartitem.cart.total_amount = sum(item.total_price for item in cartitem.cart.items.all())
            # cartitem.cart.save()

            return Response(data={"Status": "Success", "Msg": "Order Canceled S successfully"},
                            status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Order Item not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

