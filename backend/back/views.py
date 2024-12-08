from .models import User,Product,ProductCategory,Order,Review,Transportation,Payment,Favorite
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer,ProductListSerializer, CategorySerializer
from .serializers import UserSerializer,RegisterSerializer,ReviewSerializer,LoginSerializer,ProductSerializer,ReviewListSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 创建新用户
            return Response({
                'message': '用户注册成功',
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # 创建JWT Token
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'user':
                    {'id':user.id,
                    'username': serializer.validated_data['username'],
                    'email': serializer.validated_data['email'],
                    'role': serializer.validated_data['role']},     
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer =ProductSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 返回 201 状态码，表示创建成功
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 返回 400 状态码，表示数据无效
 
class CategoryListView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = CategorySerializer(categories, many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)   

class ProductView(APIView):
    def get(self,request):
        search_query = request.query_params.get('query', '')  # 获取查询的商品名称
        category_id = request.query_params.get('category', None)  # 获取查询的类别ID
        page_number = request.query_params.get('page', 1)  # 获取页码，默认是第1页
        products = Product.objects.filter(is_active=True).order_by('id') 
        if search_query:
            products = products.filter(name__icontains=search_query)
        if category_id:
            products = products.filter(category_id=category_id)
        paginator = Paginator(products, 10)
        page = paginator.get_page(page_number)
        serializer = ProductListSerializer(page.object_list, many=True)
        return Response({
            'products': serializer.data,
            'total': paginator.count
        }, status=status.HTTP_200_OK)
    
class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'category': product.category.name, 
                'owner': product.owner.id,  
            }

            return Response(product_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"detail": "商品不存在"}, status=status.HTTP_404_NOT_FOUND)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_data = request.data.get('productId')
        shipping_requirement=request.data.get('deliveryNote') 
        try:
            product = Product.objects.get(id=product_data)  # 获取产品
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        
        order_data = {
            'productid': product_data,
            'sell_user': product.owner, 
            'buy_user': request.user,  
            'total_price': product.price,
            'status': '未完成',  
            'shipping_requirement':shipping_requirement,
        }
        serializer = OrderSerializer(data=order_data, context={'request': request})
        if serializer.is_valid():
            product.is_active=False
            product.save()
            order = serializer.save()

            Payment.objects.create(
                order_id=order,
                status='待支付',  # 初始支付状态为待支付
            )

            Transportation.objects.create(
                order_id=order,
                status='待发货',  # 初始发货状态为待发货
                shipping_info='',  # 初始发货信息为空
            )

            Review.objects.create(
                order_id=order,
                reviewer_id=user,
                reviewed_user=order.sell_user,
                rating=5,  # 初始没有评分
                content=None,  # 评论内容为空
            )
            return Response({'message': 'Order created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,orderid):
        if not orderid:
            return Response({"detail": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=orderid)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != order.buy_user and request.user != order.sell_user:
            return Response({"detail": "You do not have permission to view this order."}, status=status.HTTP_403_FORBIDDEN)
        product = order.productid  
        try:
            payment = Payment.objects.get(order_id=order)
            payment_status = payment.status
        except Payment.DoesNotExist:
            payment_status = '未支付'

        # 获取与订单相关的运输信息
        try:
            transportation = Transportation.objects.get(order_id=order)
            shipping_status = transportation.status
            shipping_info=transportation.shipping_info
        except Transportation.DoesNotExist:
            shipping_status = '待发货'
            shipping_info="暂未发货请耐心等待"
        if not shipping_info:
            shipping_info="暂未发货请耐心等待"

        # 获取与订单相关的评价信息
        try:
            reviews = Review.objects.get(order_id=order)
            if reviews:
                review_content = reviews.content
            else:
                review_content = '暂无评价'
        except Review.DoesNotExist:
            review_content = '暂无评价'

        order_detail = {
            "order_id": order.id,
            "product_name": product.name,
            "product_description": product.description,
            "product_price": product.price,
            "sell_user_id":order.sell_user.id,
            "buy_user_id":order.buy_user.id,
            "order_status": order.status,
            "shipping_requirement":order.shipping_requirement,
            "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化日期
            "payment_status": payment_status,  # 支付状态
            "shipping_status": shipping_status,  # 运送状态
            "shipping_info": shipping_info,
            "review_content": review_content,  # 评价内容
        }
        return Response(order_detail, status=status.HTTP_200_OK)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_data = {
            'username': user.username,
            'rating': user.user_rating,  # 假设有 rating 字段
        }
        return Response(user_data)

class UserProductsView(APIView):
    permission_classes = [IsAuthenticated]  # 确保用户已认证

    def get(self, request):
        user = request.user  
        products = Product.objects.filter(owner=user,is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
     def get(self, request, sellerId):
        try:
            seller = User.objects.get(id=sellerId)
            serializer = UserSerializer(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "卖家信息未找到"}, status=status.HTTP_404_NOT_FOUND)

class BoughtOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            orders = Order.objects.filter(buy_user=request.user)
            if not orders.exists():
                return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
            order_data = []
            for order in orders:
                order_data.append({
                    'id':order.id,
                    'productname': order.productid.name,  # 从 Product 模型获取 productname
                    'status': order.status,  # 获取订单状态
                })
            return Response(order_data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)

        
class SoldOrdersView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.filter(sell_user=request.user)
            if not orders.exists():
                return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
            order_data = []
            for order in orders:
                order_data.append({
                    'id':order.id,
                    'productname': order.productid.name,  # 从 Product 模型获取 productname
                    'status': order.status,  # 获取订单状态
                })
            return Response(order_data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
class UserReviewsView(APIView):
    def get(self, request):
        user = request.user
        reviews = Review.objects.filter(reviewer_id=user)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserFavoritesView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user  # 获取当前认证的用户
        favorites = Favorite.objects.filter(user=user)  # 查询该用户的所有收藏
        favorite_data = []
        for favorite in favorites:
            product = favorite.product  # 获取关联的商品
            product_info = {
                'id': favorite.id,
                'productId':product.id,
                'productName': product.name,
                'productPrice': product.price,
                'productCategory': product.category.name,  # 假设商品类别是一个 ForeignKey
            }

            favorite_data.append(product_info)
        return Response(favorite_data, status=200)

class createcategory(APIView):
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response({
                'message': '目录创建成功',
                'category': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('productId')
        if not product_id:
            return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)     
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if Favorite.objects.filter(user=request.user, product=product).exists():
            return Response({"detail": "Product is already in your favorites"}, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, product=product)
        return Response({"detail": "Product added to favorites successfully"}, status=status.HTTP_201_CREATED)
    
class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('productId')
        if not product_id:
            return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        favorite = Favorite.objects.filter(user=request.user, product=product).first()
        if not favorite:
            return Response({"detail": "Product is not in your favorites"}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response({"detail": "Product removed from favorites successfully"}, status=status.HTTP_200_OK)

class CheckFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('productId')
        if not product_id:
            return Response({"detail": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        is_favorite = Favorite.objects.filter(user=request.user, product=product_id).exists()
        return Response({"isFavorite": is_favorite}, status=status.HTTP_200_OK)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        order_id = request.data.get('orderId')
        if not order_id:
            return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, id=order_id)
        payment = Payment.objects.filter(order_id=order).first()
        if not payment:
            return Response({"detail": "Payment information not found for this order."}, status=status.HTTP_404_NOT_FOUND)
        if payment.status == 'completed':
            return Response({"detail": "This order has already been paid."}, status=status.HTTP_400_BAD_REQUEST)
        payment.status = '已支付'
        payment.save()
        return Response({"detail": "Payment successful."}, status=status.HTTP_200_OK)

class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, id=order_id)
        review=Review.objects.filter(order_id=order).first()
        if not review:
            return Response({"detail": "Review information not found for this order."}, status=status.HTTP_404_NOT_FOUND)
        if review.content :
            return Response({"detail": "This order has already been review."}, status=status.HTTP_404_NOT_FOUND)
        review.rating=request.data.get('rating')
        review.content=request.data.get('content')
        review.save()
        return Response({"detail": "Review successful."}, status=status.HTTP_200_OK)
class CompleteOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # 获取请求中的 order_id
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, id=order_id)
        payment = Payment.objects.filter(order_id=order).first()
        if not payment:
            return Response({"detail": "Payment information not found for this order."}, status=status.HTTP_404_NOT_FOUND)
        transportation = Transportation.objects.filter(order_id=order).first()
        if not transportation:
            return Response({"detail": "Transportation information not found for this order."}, status=status.HTTP_404_NOT_FOUND)
        if payment.status != 'completed' and payment.status!='已支付':
            return Response({"detail": "Order has not been paid for yet."}, status=status.HTTP_400_BAD_REQUEST)
        if transportation.status != 'in_transit' and transportation.status!= '已发货':
            return Response({"detail": "Order has not been delivered yet."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = '已完成'
        order.save()

        return Response({"detail": "Order marked as completed."}, status=status.HTTP_200_OK)
    
class TransportationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        shipping_info = request.data.get('shipping_info')

        if not order_id or not shipping_info:
            return Response({"detail": "Order ID and shipping info are required."}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, id=order_id)
        transportation, created = Transportation.objects.get_or_create(order_id=order)
        transportation.shipping_info = shipping_info
        transportation.status = '已发货'
        transportation.save()
        return Response({"detail": "Shipping information updated and order marked as delivered."}, status=status.HTTP_200_OK)