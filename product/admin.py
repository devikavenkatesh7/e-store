from django.contrib import admin

from product.models import Product, Profile,Cart,Location,OrderHistory, Order,Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Location)
admin.site.register(OrderHistory)
admin.site.register(Order)
admin.site.register(Review)