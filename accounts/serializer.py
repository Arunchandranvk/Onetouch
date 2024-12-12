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

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user=self.user
        data['id']=user.id
        data['name'] = user.name
        data['address'] = user.address
        data['email'] = user.email

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



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSer(serializers.ModelSerializer):
    category_name = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field='category_name')
    images = ProductImageSerializer(many=True, source='product_img', read_only=True)  
    image_files = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=True), 
        write_only=True, 
        required=False
    )

    class Meta:
        model = Products
        fields = ['id', 'product_name', 'category_name', 'description', 'warrenty', 
                  'unit_price', 'offer_price', 'approx_time', 'stock', 'size', 
                  'images', 'image_files'] 

    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])  
        product = Products.objects.create(**validated_data)
        for image_file in image_files[:5]:  
            ProductImage.objects.create(product=product, image=image_file)
        return product
    
    def update(self, instance, validated_data):
        image_files = validated_data.pop('image_files', None)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.description = validated_data.get('description', instance.description)
        instance.warrenty = validated_data.get('warrenty', instance.warrenty)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.offer_price = validated_data.get('offer_price', instance.offer_price)
        instance.approx_time = validated_data.get('approx_time', instance.approx_time)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.size = validated_data.get('size', instance.size)
        instance.save()

        if image_files:
            instance.product_img.all().delete()  # product_img is the related_name for ProductImage
            for image_file in image_files[:5]:  
                ProductImage.objects.create(product=instance, image=image_file)
        return instance
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=['category_name','category_image']