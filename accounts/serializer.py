from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id']=user.id
        token['name'] = user.name
        token['address'] = user.address
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user=self.user
        data['id']=user.id
        data['name'] = user.name
        data['address'] = user.address
        data['email'] = user.email
        data['is_superuser'] = user.is_superuser

        return data
    
    
class Registration(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id=serializers.ReadOnlyField()
    class Meta:
        model=CustomUser
        fields=['id','name','address','email','password']
        
    def create(self,validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
    
class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','name','email','address']
        
    def create(self,validated_data):
        return CustomUser.objects.create_user(**validated_data)





class ProductSer(serializers.ModelSerializer):
    category_name = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field='category_name')

    class Meta:
        model = Products
        fields = [ 'product_name', 'category_name', 'description', 'warrenty', 
                  'unit_price', 'offer_price', 'approx_time', 'stock', 'size', 
                  'img1','img2','img3','img4','img5'] 

    def create(self, validated_data):
        product = Products.objects.create(**validated_data)
        return product
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=['category_name','category_image']


class AppoinmentSerializer(serializers.ModelSerializer):
    status=serializers.ReadOnlyField()
    class Meta:
        model = Appoinment
        fields=['user_id','service_name','address','date','time','status']

class AppoinmentStatusSerializer(serializers.ModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model = Appoinment
        fields=['id','status']



class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartItemSer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    product=ProductSer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartItemQuantitySer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [ 'quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    items = CartItemSerializer(source='items', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_amount', 'is_active', 'created_at', 'updated_at']

    def get_total_amount(self, obj):
        return sum(item.total_price for item in obj.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    product = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    shipping_address = serializers.CharField()

    class Meta:
        model = Order
        fields = ['id', 'shipping_address', 'product', 'quantity','order_items']

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data.pop('product')
        quantity = validated_data.pop('quantity')

        # Fetch the product
        product = Products.objects.get(id=product_id)
        if quantity > product.stock:
            raise serializers.ValidationError("Not enough stock available.")
        total_price = product.offer_price * quantity
        # Create the order
        order = Order.objects.create(user=user, **validated_data,total_amount=total_price)

        # Create the order item
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.offer_price
        )

        # Update the order's total amount
        # order.total_amount = total_price
        # order.save()

        # Reduce the product stock
        product.stock -= quantity
        product.save()

        return order
    

class OrderViewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    shipping_address = serializers.CharField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'shipping_address', 'total_amount', 'status', 'product_id', 'quantity']