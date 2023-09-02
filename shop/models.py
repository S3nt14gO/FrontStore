from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator , FileExtensionValidator
from uuid import uuid4
from .validators import validate_file_size


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Category(models.Model):
    title = models.CharField(max_length=100)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title',]


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)])
    quantity = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category , on_delete=models.PROTECT , related_name='products')
    promotions = models.ManyToManyField(Promotion , blank=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title',]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])
    # image = models.FileField(upload_to='store/images', validators=[FileExtensionValidator(allowed_extensions=['pdf',])])

class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('B', 'Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),
        ('P','Platinum')
    ]

    phone = models.CharField(max_length=15)
    birthdate = models.DateField(null=True)
    membership = models.CharField(max_length=1 , choices = MEMBERSHIP_CHOICES, default='B')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        db_table = 'store_customers'
        permissions = [
            ('view_history', 'Can view history')
        ]
        ordering = ['user__first_name',]
    

class Order(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),

    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=1 , choices = PAYMENT_STATUS, default='P')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order'),
        ]

class OrderedItems(models.Model):
    order = models.ForeignKey(Order , on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product , on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=9 , decimal_places=2)
 
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    customer = models.OneToOneField(Customer , on_delete= models.CASCADE , primary_key=True)

class Review(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='reviews')
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)