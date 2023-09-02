from django.urls import path , include
from rest_framework_nested import routers
from .views import *



router = routers.DefaultRouter()
router.register('products', ProductViewSet , basename='products')
router.register('categories', CategoryViewSet)
router.register('carts',CartViewSet )
router.register('customers',CustomerViewSet )
router.register('orders',OrderViewSet , basename='orders')


products_router = routers.NestedDefaultRouter(router , 'products', lookup='product') # in lookup means product_pk
products_router.register('reviews', ReviewViewSet , basename='product-reviews')
products_router.register('images', ProductImageViewset , basename='product-images')
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items',CartItemViewSet, basename='cart-items') 


# urlpatterns = [
#     path('', include(router.urls)),

    # path('products/', ProductList.as_view()),
    # path('products/<int:id>/', ProductDetails.as_view()),
    # path('categories/', CategryList.as_view()),
    # path('categories/<int:pk>/', CategoryDetails.as_view()),
# ]

urlpatterns = router.urls + products_router.urls + carts_router.urls
