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
            print(ser.data)
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
            return Response(data={"Msg": "All Products","data":pro.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
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
            if product.user!=request.user:
                return Response(data={"Status":"Failed","Msg":"Unauthorized access: You do not have permission to modify this product."},status=status.HTTP_401_UNAUTHORIZED)
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
            print(request.user)
            if product.user!=request.user:
                return Response(data={"Status":"Failed","Msg":"Unauthorized access: You do not have permission to delete this product."},status=status.HTTP_401_UNAUTHORIZED)
            product.delete()
            return Response({"Status":"Success","Msg":f"{product.name} Deleted Successfully!!!!!"})
        except Exception as e:
            return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllProductsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            products=Products.objects.all()
            pro=ProductSer(products,many=True)
            return Response(data={"Msg": "All Products","data":pro.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)