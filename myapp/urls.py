from django.urls import path
from . import views
from .views import forgot_password, verify_otp, reset_password, download_invoice

urlpatterns = [
    # ✅ Home & Auth
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # ✅ Password Reset
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("reset-password/", reset_password, name="reset_password"),

    # ✅ Contact Form
    path("contact/", views.ContactView.as_view(), name="contact"),

    # ✅ Product Management
    path("product/", views.product, name="product"),
    path("product_detail/<int:pid>/", views.product_detail, name="product_detail"),
    path("catfilter/<str:cv>/", views.catfilter, name="catfilter"),
    path("sortfilter/<str:sv>/", views.sortfilter, name="sortfilter"),
    path("pricefilter/", views.pricefilter, name="pricefilter"),
    path("srcfilter/", views.srcfilter, name="srcfilter"),

    # ✅ Cart & Orders
    path("addtocart/<int:pid>/", views.addtocart, name="addtocart"),
    path("cart/", views.cart, name="cart"),
    path("updateqty/<str:x>/<int:cid>/", views.updateqty, name="updateqty"),
    path("remove/<int:cid>/", views.remove, name="remove"),
    path("placeorder/", views.placeorder, name="placeorder"),
    path("fetchorder/", views.fetchorder, name="fetchorder"),

    # ✅ Payment & Invoice
    path("makepayment/", views.makepayment, name="makepayment"),
    path("paymentsuccess/", views.paymentsuccess, name="payment-success"),
    path("download_invoice/<int:order_id>/", download_invoice, name="download_invoice"),
]

