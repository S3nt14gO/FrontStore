from django.shortcuts import render ,HttpResponse
from django.core.mail import send_mail , mail_admins , BadHeaderError , EmailMessage 
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from templated_mail.mail import BaseEmailMessage
from django.db.models import Q , F , Value , Func , ExpressionWrapper , DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count , Max , Min , Avg , Sum
from rest_framework.views import APIView
from shop.models import Product , OrderedItems , Order , Customer , Category
from tags.models import TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.db import transaction , connection
from .tasks import notify_customers
import logging
import requests

logger = logging.getLogger(__name__) #playground.views




class HelloView(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Recevied the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
        return render(request,'hello.html', {'user':data})



# @cache_page(5 * 60)
# def hello(r):
    # products =  Product.objects.all()
    # for pro in products:
    #     print(pro)  

    # products =  Product.objects.filter(last_update__year=2021) 

    # products =  Product.objects.filter(quantity__lt=10 , price__lt=20)  #multi filtering
    # products = Product.objects.filter(quantity__lt=10).filter(price__lt=20)  #filter of filtered
    # products =  Product.objects.filter(Q(quantity__lt=10) | Q(price__lt=20)) #or
    # products =  Product.objects.filter(Q(quantity__lt=10) & Q(price__lt=20)) #and
    # products =  Product.objects.filter(Q(quantity__lt=10) & ~Q(price__lt=20)) #telda means without

    # products =  Product.objects.filter(quantity =F('category__id')) # F to make column can equal other column

    # products =  Product.objects.order_by('title') # sort ASC
    # products =  Product.objects.order_by('-title') # sort DESC
    # products =  Product.objects.order_by('price','-title') # the same price will be DESC sorted
    # products =  Product.objects.order_by('price','-title').reverse() # reverse order

    # products =  Product.objects.filter(category__id=3).order_by('price') 
      
    # products =  Product.objects.all()[:50]

    # products =  Product.objects.values('id','title','category__title')[:50] #inner join
    # products =  Product.objects.values_list('id','title','category__title')[:50] #tuple of values without column name
    # products = OrderedItems.objects.values('product_id').order_by('product_id').distinct() #avoid duplicates

    # products = Product.objects.filter(
    #     id__in=OrderedItems.objects.values('product_id').distinct()
    # ) # filter products object by ordered items 

    # products = Product.objects.select_related('category').all()  # select all without more quries loaded
    # products = Product.objects.prefetch_related('promotions').select_related('category').all() #inner joins
    # products = Order.objects.select_related('customer').prefetch_related('items__product').order_by('-placed_at')[:5] #last 5 orders related to customers with the ordered items

    # result = Product.objects.filter(category__id=3).aggregate(count=Count('id') , min_price = Min('price'))

    #annotate to use Expression

    # products = Customer.objects.annotate(is_new=Value(True)) # add new column with value True

    # products = Customer.objects.annotate(new_id=F('id') +1) # add new Column reference to id and increase it's value by 1

    # products = Customer.objects.annotate(
    #     #Concat
    #     full_name = Func(F('first_name'), Value(' ') , F('last_name'),function='CONCAT') # Concat full name and Value ' ' between first and last name
        
    # )
    # products = Customer.objects.annotate(
    #     #Concat
    #     full_name = Concat('first_name', Value(' ') ,'last_name') # Concat full name and Value ' ' between first and last name
    # )

    # products = Customer.objects.annotate(
    #     orders_count = Count('order') # number of orders for each  customer from order table and ordered by DESC 
    # ).order_by('orders_count').reverse()


    # discounted_pricex = ExpressionWrapper(
    #     F('price') * 0.8, output_field=DecimalField())  

    # products = Product.objects.annotate(
    #     discounted_price = discounted_pricex   # add new column Discount_price with new value
    # )

    # Category.objects.filter(id=11).delete()

    # with transaction.atomic():
    # products = Product.objects.raw('SELECT * FROM shop_product') # SQL query

    # with connection.cursor() as cursor:
    #     cursor.callproc('get_customers',[1,2,3,4,'a']) # much better than writing raw sql queries
    # try:
        # send_mail('Hola Amigo', "SMTP server Esht3'l",'HaithamLover@company', ['ahmed.abdelnasser7777777@gmail.com'])
        # mail_admins('subject','message', html_message='message')
        # message = EmailMessage('subject','message','HaithamLover@company',['ahmed.abdelnasser7777777@gmail.com'] )
        # message.attach_file('playground/static/images/killu.jpg')
        # message.send()

    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name':'Ahmed'}
    #     )
        
    #     message.send(['ahmed.abdelnasser7777777@gmail.com'])
    # except BadHeaderError:
    #     pass

    # notify_customers.delay('Hello')


    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(key, data)
    
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()

    # return render(r,'hello.html', {'user':data})

# , 'results' : list(products)