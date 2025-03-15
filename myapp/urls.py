from django.urls import path
from . import views
from .views import forgot_password, verify_otp, reset_password

urlpatterns = [
        path("",views.index,name='index'),
        # path("/home",views.index,name='index'),
        path("register/",views.register,name='register'),
        path("login/",views.user_login,name='login'),
        path("logout/",views.user_logout,name='logout'),
        path("forgot-password/", forgot_password, name="forgot_password"),
        path("verify-otp/", verify_otp, name="verify_otp"),
        path("reset-password/", reset_password, name="reset_password"),
        path('contact/', views.ContactView.as_view(), name='contact'),
        path('product/',views.product,name="product"),  
        path('catfilter/<cv>',views.catfilter),
        path('sortfilter/<sv>',views.sortfilter),
        path('pricefilter',views.pricefilter),
        path('product_detail/<pid>',views.product_detail),
        path('addtocart/<pid>',views.addtocart),
        path('cart',views.cart),
        path('updateqty/<x>/<cid>',views.updateqty),
        path('remove/<cid>',views.remove),
        path('placeorder',views.placeorder),
        path('fetchorder',views.fetchorder),
        path('srcfilter',views.srcfilter,name='srcfilter'),

]

