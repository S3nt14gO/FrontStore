from typing import Any, List, Optional, Tuple
from django.contrib import admin , messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Category , Customer , Product , Order , OrderedItems , Cart , CartItems , ProductImage
from django.db.models import Q , F , Value 
from django.db.models.aggregates import Count 
from django.utils.html import format_html , urlencode  
from django.urls import reverse




class QuantityFilter(admin.SimpleListFilter):
    title = 'quantity'
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return [
            ('<10' ,'low')

        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
           return queryset.filter(quantity__lt=10)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']
    max_num = 5
    extra = 0

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"') 
        return ''

    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields ={ # auto complete Slug field as per title
        'slug': ['title']  
    }
    exclude = ['promotions']  # exclude promotions fields from product
    actions = ['clear_inventory']
    
    list_display = ['title', 'price' , 'quantity_status', 'category']
    list_editable = ['price']
    list_filter = ['category' , 'last_update' , QuantityFilter]
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['title__istartswith']


    @admin.display(ordering='quantity')
    def quantity_status(self, Product):
        if Product.quantity < 10:
            return 'Low'
        else :
            return 'Good'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(quantity = 0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['styles.css']
        }



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self , category):
        url = reverse('admin:shop_product_changelist') + '?' + urlencode({
            'category__id' : str(category.id)
        })
          # admin_appname_model_page
        return format_html ('<a href="{}">{}</a>',url , category.products_count) 
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self , customer):
        url = reverse('admin:shop_order_changelist') + '?' + urlencode({
            'customer__id' : str(customer.id)
        })
        return format_html ('<a href="{}">{} </a>',url , customer.orders_count) 
    
    def get_queryset(self, request):

        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
    

class OrderItemInLine(admin.TabularInline):   # inherited from Order  Inline Inputs
# class OrderItemInLine(admin.StackedInline): # Block Inputs 
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = OrderedItems  
    extra = 0  # number of columns

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['payment', 'customer']
    inlines = [OrderItemInLine]
    autocomplete_fields = ['customer']


class CartItemInLine(admin.TabularInline): 
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = CartItems
    extra = 0  # number of columns

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    inlines = [CartItemInLine]
