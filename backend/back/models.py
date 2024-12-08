from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户模型
class User(AbstractUser):
    USER_ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员'),
    ]
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
    user_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # 自定义反向访问名称
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # 自定义反向访问名称
        blank=True
    )
    def __str__(self):
        return self.username


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 目录名称
    description = models.TextField(blank=True, null=True)  # 目录描述
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)  # 商品名称
    description = models.TextField(blank=True, null=True)  # 商品描述
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 商品价格
    owner=models.ForeignKey(User,on_delete=models.CASCADE)#卖家
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')  # 商品目录
    is_active = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.name


class Order(models.Model):
    productid=models.ForeignKey(Product,on_delete=models.CASCADE)
    sell_user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='sell_orders',)  #买家
    buy_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_orders', ) #卖家
    order_date = models.DateTimeField(auto_now_add=True)  # 订单日期
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 价格
    shipping_requirement = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', '未完成'), ('completed', '已完成'), ('canceled', '取消')],
        default='未完成'
    )  # 订单状态

    def __str__(self):
        return f"Order #{self.id} by {self.sell_user.username} to {self.buy_user.username}"

class Review(models.Model):#TODO 补全评论的属性
    review_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    reviewer_id = models.ForeignKey(User, related_name='reviews_written', on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} for Order {self.order_id}"

class Transportation(models.Model):
    Shipping_Info_STATUS_CHOICES = [
        ('pending', '待发货'),
        ('in_transit', '已发货'),
        ('delivered', '已送达'),
    ]

    shipping_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_info = models.CharField(max_length=200,blank=True, null=True)
    status = models.CharField(max_length=20, choices=Shipping_Info_STATUS_CHOICES)

    def __str__(self):
        return f"Shipping_Info {self.shipping_id} for Order {self.order_id}"

class Payment(models.Model):
    status_choices = [
        ('pending', '待支付'),
        ('completed', '已支付'),
    ]
    order_id = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=status_choices, default='pending')  # 支付状态
    payment_date = models.DateTimeField(auto_now_add=True)  # 记录支付日期

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 用户收藏的商品
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favorite: {self.user.username} - {self.product.name}"

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    buyer_id = models.ForeignKey(User, related_name='buyer_chats', on_delete=models.CASCADE)
    seller_id = models.ForeignKey(User, related_name='seller_chats', on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    message_content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.message_id} between {self.buyer_id.username} and {self.seller_id.username}"

