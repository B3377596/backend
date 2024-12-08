# admin.py
from django.contrib import admin
from .models import User, Order, Product, ProductCategory

# 注册 User 模型
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')
    search_fields = ('username', 'email')

# 注册 Order 模型
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'status')
    search_fields = ('order_id', 'user__username')

# 注册 Product 模型
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

# 注册 Category 模型
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# 注册模型到 Django 后台管理
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
