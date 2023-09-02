
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view , action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin , CreateModelMixin , RetrieveModelMixin , DestroyModelMixin , UpdateModelMixin
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView 
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser , DjangoModelPermissions
# from rest_framework.pagination import PageNumberPagination
from .models import Product , Category , OrderedItems , Review , Cart , CartItems , Customer , Order , ProductImage
from .serializers import ProductSerializer , CategorySerializer , ReviewSerializer , CartItemSerializer , CartSerializer , AddCartItemSerializer , UpdateCartItemSerializer , CustomerSerializer , OrderSerializer , CreateOrderSerializer , UpdateOrderSerializer , ProductImageSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly , FullDjangoModelPermissions , ViewCustomerHistoryPermission

RetrieveUpdateDestroyAPIView

# class ProductList(APIView):  # mixins
#       def get(self , request):
#             product = Product.objects.select_related('category').all()
#             serializer = ProductSerializer(product, many=True , context = {
#                 'request': request
#             })
#             return Response(serializer.data) 
      
#       def post(self , request):
#             serializer = ProductSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_201_CREATED)      


# class ProductList(ListCreateAPIView):   #Generic Mixins
#       queryset = Product.objects.select_related('category').all()
#       serializer_class = ProductSerializer
      
#       def get_serializer_context(self):
#              return {'request': self.request}
      
#       def post(self , request):
#             serializer = ProductSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_201_CREATED)   


class ProductViewSet(ModelViewSet):
      queryset = Product.objects.prefetch_related('images').all()
      # queryset = Product.objects.all()
      serializer_class = ProductSerializer
      filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
      filterset_class = ProductFilter
      pagination_class = DefaultPagination
      permission_classes = [IsAdminOrReadOnly]
      search_fields = ['title', 'description']
      ordering_fields = ['price', 'last_update']

      def get_serializer_context(self):
          return {'request': self.request}
      
      def destroy(self, request, *args, **kwargs):
            if OrderedItems.objects.filter(product_id=kwargs['pk']).count() > 0 :  
                  return Response({'error':'Product cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return super().destroy(request, *args , **kwargs)

class ProductImageViewset(ModelViewSet):
      serializer_class = ProductImageSerializer
      
      def get_queryset(self):
            return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
      
      def get_serializer_context(self):
          return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
      queryset = Cart.objects.prefetch_related('items__product').all()
      serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
      http_method_names = ['get', 'post', 'patch', 'delete']  #make the http methods only supports the selected methods

      def get_serializer_class(self):
            if self.request.method == 'POST':
                  return AddCartItemSerializer
            elif self.request.method == 'PATCH':
                  return UpdateCartItemSerializer
            return CartItemSerializer

      def get_serializer_context(self):
            return {'cart_id': self.kwargs['cart_pk']}

      def get_queryset(self):
            return CartItems.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

# class ProductList(ListCreateAPIView):  
#       queryset = Product.objects.select_related('category').all()
#       serializer_class = ProductSerializer
      
#       def get_serializer_context(self):
#              return {'request': self.request}
      
#       def post(self , request):
#             serializer = ProductSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_201_CREATED)  

# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         product = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(product, many=True , context = {
#                 'request': request
#         })
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data , status=status.HTTP_201_CREATED)

# @api_view()
# def product_details(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
# class ProductDetails(APIView):
      
#       def get(self , request, id):
#             product = get_object_or_404(Product, pk=id)
#             serializer = ProductSerializer(product)
#             return Response(serializer.data)

#       def put(self , request, id):
#               product = get_object_or_404(Product, pk=id)
#               serializer = ProductSerializer(product ,data = request.data)
#               serializer.is_valid(raise_exception=True)
#               serializer.save()  
#       def delete(self , request, id):
              
#               product = get_object_or_404(Product, pk=id)
#               if product.orderitems.count() > 0:
#                     return Response({'error':'Product cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#               product.delete()
#               return Response(status=status.HTTP_204_NO_CONTENT)       

# class ProductDetails(RetrieveUpdateDestroyAPIView):
#       queryset = Product.objects.all()
#       serializer_class = ProductSerializer
#       lookup_field = 'id'
      
#       def delete(self , request, id):
              
#               product = get_object_or_404(Product, pk=id)
#               if product.orderitems.count() > 0:
#                     return Response({'error':'Product cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#               product.delete()
#               return Response(status=status.HTTP_204_NO_CONTENT)   

# class ProductDetails(RetrieveUpdateDestroyAPIView):

#       lookup_field = 'id'
      
               
              

# @api_view(['GET','PUT', 'DELETE'])
# def product_details(request, id):
#         product = get_object_or_404(Product, pk=id)
#         if request.method =="GET":
#                 serializer = ProductSerializer(product)
#                 return Response(serializer.data)
#         elif request.method == "PUT":
#               serializer = ProductSerializer(product ,data = request.data)
#               serializer.is_valid(raise_exception=True)
#               serializer.save()
#               return Response(serializer.data)
#         elif request.method == "DELETE":
#               if product.orderitems.count() > 0:
#                     return Response({'error':'Product cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#               product.delete()
#               return Response(status=status.HTTP_204_NO_CONTENT)




class CategoryViewSet(ModelViewSet):
      queryset = Category.objects.annotate(
              products_count = Count('products')).all()
      serializer_class = CategorySerializer
      permission_classes = [IsAdminOrReadOnly]

      # def destroy(self, request, *args, **kwargs):
      #       if OrderedItems.objects.filter(product_id=kwargs['pk']).count() > 0 :  
      #             return Response({'error':'Product cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      #       return super().destroy(request, *args , **kwargs)

      def delete(self , request, pk):
            category = get_object_or_404(Category, pk=pk)
            if category.products.count() > 0:
                  return Response({'error':'Category cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
      serializer_class = ReviewSerializer

      def get_queryset(self):
            return Review.objects.filter(product_id = self.kwargs['product_pk'])

      def get_serializer_context(self):
            return {'product_id': self.kwargs['product_pk']}


class CustomerViewSet(ModelViewSet):
      queryset = Customer.objects.all()
      serializer_class = CustomerSerializer
      
      permission_classes = [IsAdminUser]
      # permission_classes = [FullDjangoModelPermissions]

      # def get_permissions(self):
      #       if self.request.method == 'GET':
      #             return [AllowAny()]
      #       # if self.request.method == 'PUT':
      #       return [IsAuthenticated()]

      @action(detail=True,  permission_classes =[ViewCustomerHistoryPermission])
      def history(self, request, pk):
            return Response("ok")

      @action(detail=False, methods=['GET', 'PUT'], permission_classes =[IsAuthenticated])
      def me(self , request):
            # (customer , created) = Customer.objects.get_or_create(user_id=request.user.id)
            customer= Customer.objects.get(user_id=request.user.id)
            if request.method == 'GET':
                  serializer = CustomerSerializer(customer)
                  return Response(serializer.data)
            elif request.method == 'PUT':
                  serializer = CustomerSerializer(customer , data=request.data)
                  serializer.is_valid(raise_exception=True)
                  serializer.save()
                  return Response(serializer.data)

                  
class OrderViewSet(ModelViewSet):
      http_method_names = ['get','post', 'patch', 'delete', 'head', 'options']
      def get_permissions(self):
            if self.request.method in ['PUT', 'PATCH', 'DELETE']:
                  return [IsAdminUser()]
            return [IsAuthenticated()]


      def create(self, request, *args , **kwargs):
            serializer = CreateOrderSerializer(data=request.data , context ={'user_id': self.request.user.id})
            serializer.is_valid(raise_exception=True)
            order =serializer.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)

      def get_serializer_class(self):
            if self.request.method == 'POST':
                 return CreateOrderSerializer
            elif self.request.method == 'PATCH':
                  return UpdateOrderSerializer
            return OrderSerializer

      def get_queryset(self):
            user = self.request.user
            if user.is_staff:
                  return Order.objects.all()
            # (customer_id, created) =Customer.objects.only('id').get_or_create(user_id=user.id)
            # return Order.objects.filter(customer_id=customer_id)
      
            customer_id=Customer.objects.only('id').get(user_id=user.id)
            return Order.objects.filter(customer_id=customer_id)



# @api_view(['GET','POST'])
# def category_list(request):
#         if request.method == 'GET':
#               queryset = Category.objects.annotate(products_count=Count('products'))
#               serializer = CategorySerializer(queryset , many=True)
#               return Response(serializer.data)
#         elif request.method == 'POST':
#               serializer = CategorySerializer(data=request.data)
#               serializer.is_valid(raise_exception=True)
#               serializer.save()
#               return Response(serializer.data , status=status.HTTP_201_CREATED)
#         return Response('Ok')

# @api_view(['GET','PUT', 'DELETE'])      
# def category_details(request, pk):
#         category = get_object_or_404(
#               Category.objects.annotate(
#               products_count=Count('products')), pk=pk)
#         if request.method == 'GET':
#               serializer = CategorySerializer(category)
#               return Response(serializer.data)
#         elif request.method =='PUT':
#               serializer = CategorySerializer(category , data=request.data)
#               serializer.is_valid(raise_exception=True)
#               serializer.save()
#               return Response(serializer.data)
      #   elif request.method == "DELETE":
      #         if category.products.count() > 0:
      #               return Response({'error':'Category cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      #         category.delete()
      #         return Response(status=status.HTTP_204_NO_CONTENT)
      #   return Response('Ok')

  
# class CategoryDetails(RetrieveUpdateDestroyAPIView):
#       queryset = Category.objects.annotate(
#             products_count = Count('products')
#       )
#       serializer_class = CategorySerializer

#       def delete(self , request, pk):
#             category = get_object_or_404(Category, pk=pk)
#             if category.products.count() > 0:
#                   return Response({'error':'Category cannot be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             category.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
