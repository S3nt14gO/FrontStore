from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from shop.admin import ProductAdmin , ProductImageInline
from tags.models import TaggedItem
from shop.models import Product
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email","first_name", "last_name" ),
            },
        ),
    )



class TagInLine(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    max_num = 10
    extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine , ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product , CustomProductAdmin)