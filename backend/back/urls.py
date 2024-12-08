from django.urls import path
from django.conf import settings
from django.shortcuts import redirect
from .views import RegisterView,LoginView
from .views import CreateOrderView,ProductCreateView,CategoryListView,ProductDetailView,UserDetailView,createcategory,ProductView,OrderDetailView,ReviewView
from .views import SoldOrdersView,UserProductsView,UserFavoritesView,BoughtOrdersView,UserProfileView,PaymentView,TransportationView,CompleteOrderView,UserReviewsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AddFavoriteView, RemoveFavoriteView, CheckFavoriteView

def redirect_to_admin(request):
    return redirect('http://localhost:8000/admin') 

urlpatterns=[#登录注册相关
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login',LoginView.as_view()),
    path('api/register',RegisterView.as_view(), name='register'),
    path('admin/', redirect_to_admin),
]

urlpatterns+=[#商品订单相关
    path('api/createorders',CreateOrderView.as_view()),
    path('api/createproducts',ProductCreateView.as_view()),
    path('api/searchproducts',ProductView.as_view()),
    path('api/categories',CategoryListView.as_view(),name='showcategories'),
    path('api/products/<int:product_id>',ProductDetailView.as_view()),
    path('api/createcategory',createcategory.as_view()),
    path('api/user/<int:sellerID>',UserDetailView.as_view()),
    path('api/orderdetail/<int:orderid>',OrderDetailView.as_view()),
    path('api/payment',PaymentView.as_view()),
    path('api/transportation',TransportationView.as_view()),
    path('api/completeorder',CompleteOrderView.as_view()),
    path('api/review',ReviewView.as_view()),
]

urlpatterns+=[#个人主页相关
    path('api/user/bought-orders', BoughtOrdersView.as_view(), name='bought-orders'),
    path('api/user/sold-orders',SoldOrdersView.as_view()),
    path('api/user/favorites',UserFavoritesView.as_view()),
    path('api/user/products',UserProductsView.as_view()),
    path('api/profile',UserProfileView.as_view()),
    path('api/user/reviews',UserReviewsView.as_view()),
]

urlpatterns += [
    path('api/addfavorites', AddFavoriteView.as_view(), name='add_favorite'),
    path('api/removefavorites', RemoveFavoriteView.as_view(), name='remove_favorite'),
    path('api/checkfavorites', CheckFavoriteView.as_view(), name='check_favorite'),
]

