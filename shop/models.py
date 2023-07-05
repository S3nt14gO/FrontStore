from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Category(models.Model):
    title = models.CharField(max_length=100)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category , on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('B', 'Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),
        ('P','Platinum')
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15)
    birthdate = models.DateField(null=True)
    membership = models.CharField(max_length=1 , choices = MEMBERSHIP_CHOICES, default='B')

    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields = ['first_name', 'last_name'])
            ]
    

class Order(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),

    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(max_length=1 , choices = PAYMENT_STATUS, default='P')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderedItems(models.Model):
    order = models.ForeignKey(Order , on_delete=models.PROTECT)
    product = models.ForeignKey(Product , on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=9 , decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    customer = models.OneToOneField(Customer , on_delete= models.CASCADE , primary_key=True)