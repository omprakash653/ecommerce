from django.urls import path
from . import views

urlpatterns = [
        path("",views.index,name='index'),
        # path("/home",views.index,name='index'),
        path("register",views.register,name='register'),
        path("login",views.user_login,name='login'),
        # path("contact",views.contact,name='contact'),
        path('contact/', views.ContactView.as_view(), name='contact'),
]

