from decimal import Decimal
from rest_framework import serializers 
from django.db import transaction
from django.core.validators import MinValueValidator
from .signals import order_created

from .models import Product , Category , Review , Cart , CartItems , Customer , Order , OrderedItems, ProductImage


# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=100) 
class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
    class Meta:
        model = ProductImage
        fields = ['id','image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True , read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description' ,'price','slug','quantity','category', 'price_with_tax', 'images']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self , product:Product):
        return product.price * Decimal(1.1)



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','price']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only = True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date' ]

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id , **validated_data)
    


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItems):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItems
        fields = ['id', 'product', 'quantity', 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('no product with the given ID was found')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItems.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItems.DoesNotExist:
            self.instance = CartItems.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance

    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True )
    items = CartItemSerializer(many=True , read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([ item.quantity * item.product.price for item in cart.items.all()])
        
    
    class Meta:
        model = Cart
        fields = ['id' , 'items' , 'total_price' ]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birthdate', 'membership']



class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderedItems
        fields = ['id','product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer','placed_at', 'payment', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment']


class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic():
        cart_id = serializers.UUIDField()

        def validate_cart_id(self ,cart_id):
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError(' No cart with the give id was found')
            if CartItems.objects.filter(cart_id=cart_id).count() == 0:
                raise serializers.ValidationError('Cart is Empty')
            return cart_id

        def save(self, **kwargs):
            cart_id = self.validated_data['cart_id']
            # (customer,created)=Customer.objects.get_or_create(user_id = self.context['user_id'])
            customer=Customer.objects.get(user_id = self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItems.objects.select_related('product').filter(cart_id =cart_id )
            order_items = [
                OrderedItems(
                    order =order,
                    product = item.product,
                    unit_price = item.product.price,
                    quantity = item.quantity
                ) for item in cart_items]
            OrderedItems.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__ , order = order)

            return order


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=100)
#     price = serializers.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)])
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset = Category.objects.all()
    # )
    # category = serializers.StringRelatedField()
    # category = CategorySerializer()
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'category-details'
    # )



    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.price = validated_data.get('price')
    #     instance.save()
    #     return instance
    



    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return