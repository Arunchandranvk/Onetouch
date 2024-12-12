from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:
            try:
                validate_password(password, user)
            except ValidationError as e:
                raise ValueError(f"Password validation error: {e.messages}")
            user.set_password(password)
        else:
            raise ValueError("Password is required")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(unique=True)
    address=models.TextField(blank=True,null=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email
    


class Categories(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='cat_user')
    category_name=models.CharField(max_length=200)
    category_image=models.ImageField(upload_to='Category Images')

    def __str__(self):
        return self.category_name
    

class Products(models.Model):
    product_name=models.CharField(max_length=200)
    category_name=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='product_cat')
    description=models.TextField()
    warrenty=models.CharField(max_length=100)
    unit_price=models.IntegerField()
    offer_price=models.IntegerField()
    approx_time=models.CharField(max_length=100)
    stock=models.IntegerField(null=True,blank=True)
    size=models.IntegerField()
    datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
class ProductImage(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_img')
    image=models.ImageField(upload_to='products')

    def __str__(self):
        return self.product_id.product_name


class Cart(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user_id.get_username}"
    
class CartItem(models.Model):
    cart_id=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_user')
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in {self.cart.user.username}'s cart"
    
class Order(models.Model):
    user_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status=models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Order {self.order.id}"
    
class Appointment(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    service_name=models.CharField(max_length=200)
    address=models.TextField()
    date=models.DateField()
    time=models.TimeField()

    def __str__(self):
        return self.service_name