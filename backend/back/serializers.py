from rest_framework import serializers
from .models import Order,ProductCategory,Product,User,Review,Favorite
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
from django.utils import timezone

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("无效的用户名或密码")
        
        # 返回用户信息
        return {
            'user': user,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'user_rating': user.user_rating,
        }
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # 创建用户对象
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role = validated_data.get('role', 'user'), # 默认角色为 'user'
            phone_number = validated_data.get('phone_number', '')  # 默认空的电话号码
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields =['id','name', 'description']

# 商品序列化器
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price', 'category','owner']
        read_only_fields = ['owner']  

    # 创建商品时，处理传入的商品分类数据
    def create(self, validated_data):    
        return super().create(validated_data)

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id",'name','price']
    

class OrderSerializer(serializers.ModelSerializer):
    productid = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # 外键字段
    sell_user = serializers.PrimaryKeyRelatedField(read_only=True)  # 卖家是只读字段
    buy_user = serializers.PrimaryKeyRelatedField(read_only=True)  # 买家是只读字段
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)  # 总价字段
    status = serializers.CharField(default='未完成')  # 默认订单状态
    order_date = serializers.DateTimeField(read_only=True)  # 订单日期是只读字段
    
    class Meta:
        model = Order
        fields = ['id','productid', 'sell_user', 'buy_user', 'total_price', 'status', 'order_date','shipping_requirement']

    def create(self, validated_data):
        # 获取当前用户
        user = self.context['request'].user
        validated_data['buy_user'] = user  # 设置 buy_user 为当前请求的用户
        validated_data['status'] = '未完成'  # 默认订单状态为 'pending'

        # 获取产品信息并填充 sell_user 和 total_price
        product = validated_data['productid']
        validated_data['sell_user'] = product.owner  # 卖家为产品的拥有者
        validated_data['total_price'] = product.price  # 总价为产品价格
        validated_data['order_date'] = timezone.now()  # 订单创建时间为当前时间

        # 创建并返回订单对象
        order = Order.objects.create(**validated_data)
        return order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'rating']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'order_id', 'reviewer_id', 'reviewed_user', 'rating', 'content', 'created_at']
        read_only_fields = ['review_id', 'created_at', 'reviewer_id']

    def create(self, validated_data):
        return super().create(validated_data)
    
class ReviewListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='order_id.productid.name')
    comment = serializers.CharField(source='content')
    rating = serializers.IntegerField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = Review
        fields = ['product_name', 'comment', 'rating', 'created_at']


