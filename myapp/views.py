from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt  # Only use if CSRF is causing issues
from django.views.decorators.csrf import csrf_protect # Protects all methods from CSRF attacks
from .models import Contact,Product,Cart,Order
from django.contrib import messages
from django.db import IntegrityError, DatabaseError
import re
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import now
import random
########################################
def index(request):
    return render(request,'home.html')

########################################

import re
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        try:
            uname = request.POST.get("uname")
            uemail = request.POST.get("uemail")
            upass = request.POST.get("upass")
            ucpass = request.POST.get("ucpass")

            # Validate form data
            if not uname or not uemail or not upass or not ucpass:
                messages.error(request, "All fields are required.")
                return redirect("register")

            if upass != ucpass:
                messages.error(request, "Passwords do not match.")
                return redirect("register")

            if len(upass) < 6:
                messages.error(request, "Password must be at least 6 characters long.")
                return redirect("register")

            if not re.search(r'[A-Za-z]', upass) or not re.search(r'[0-9]', upass):
                messages.error(request, "Password must contain both letters and numbers.")
                return redirect("register")

            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already taken.")
                return redirect("register")

            if User.objects.filter(email=uemail).exists():
                messages.error(request, "Email already registered.")
                return redirect("register")

            
            user = User.objects.create_user(username=uname, email=uemail, password=upass)
            user.save()
            # Send welcome email
            subject = "Welcome to Shopping Kart 🎉"
            message = f"""
            Hi {uname}, 

            Welcome to Shopping Kart! 🛒
            
            We're thrilled to have you onboard. Start exploring our latest products and enjoy seamless shopping.

            🚀 **Exclusive Benefits Await You:**
            - Get the best deals on trending products
            - Fast and secure checkout
            - 24/7 customer support

            Happy Shopping! 🛍️

            Regards,  
            **Shopping Kart Team**
            """
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [uemail]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Success message and redirect to login
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")

        except IntegrityError:
            messages.error(request, "Database error. Please try again.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, "register.html")


########################################

from django.contrib.auth import authenticate, login, logout
def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        n = request.POST.get('uname', '').strip()
        p = request.POST.get('upass', '').strip()

      
        u = authenticate(username=n, password=p)

        if u is not None:
            login(request, u)
            messages.success(request, "Login successful!")
            return redirect("/")  
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect("login")

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")
###################################################################################################forget
# Store OTPs temporarily
otp_storage = {}

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_storage[email] = {"otp": otp, "time": now()}  # Save OTP & timestamp

            # Send OTP via email
            subject = "Password Reset OTP - Shopping Kart"
            message = f"""
            Hello {user.username},

            You requested a password reset. Use the OTP below to proceed:
            
            🔢 Your OTP: {otp}

            This OTP is valid for 10 minutes.

            If you didn't request this, please ignore this email.

            Regards,
            Shopping Kart Team
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            messages.success(request, "OTP has been sent to your email.")
            return redirect("verify_otp")

        except User.DoesNotExist:
            messages.error(request, "Email not registered!")
            return redirect("forgot_password")

    return render(request, "forgot_password.html")


def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp_entered = request.POST.get("otp")

        if email in otp_storage:
            otp_data = otp_storage[email]
            otp_correct = otp_data["otp"]

            if str(otp_entered) == str(otp_correct):
                messages.success(request, "OTP verified! Set a new password.")
                return redirect("reset_password")
            else:
                messages.error(request, "Invalid OTP! Please try again.")
                return redirect("verify_otp")
        else:
            messages.error(request, "OTP expired or invalid.")
            return redirect("forgot_password")

    return render(request, "verify_otp.html")


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("reset_password")

        if len(new_password) < 6 or not any(char.isdigit() for char in new_password) or not any(char.isalpha() for char in new_password):
            messages.error(request, "Password must be at least 6 characters long and contain both letters and numbers.")
            return redirect("reset_password")

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # Clear OTP after successful reset
            otp_storage.pop(email, None)

            messages.success(request, "Password reset successful! You can log in now.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "Error resetting password. Please try again.")

    return render(request, "reset_password.html")


########################################
# @method_decorator(csrf_exempt, name='dispatch')  # Apply decorator to all methods
@method_decorator(csrf_protect, name='dispatch')  # Protects all methods from CSRF attacks
class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            name = request.POST.get('name').strip()
            contact = request.POST.get('contact').strip()
            email = request.POST.get('email').strip()
            description = request.POST.get('description')

            errors = []
            if not name:
                errors.append("Name is required.")
            if not contact.isdigit() or len(contact) < 10:
                errors.append("Enter a valid contact number (at least 10 digits).")
            if "@" not in email or "." not in email:
                errors.append("Enter a valid email address.")
            if not description:
                errors.append("Description cannot be empty.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, self.template_name) 
            Contact.objects.create(name=name, contact=contact, email=email, description=description)

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  
        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist.")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return render(request, self.template_name)  


def product(request):
    p=Product.objects.filter(is_active=True)
    # print(p)
    context={}
    context['data']=p
    return render(request,'product.html',context)

from django.db.models import Q
# def catfilter(request,cv):
#     # print(cv)
#     q1=Q(cat=cv)
#     q2=Q(is_active=True)

#     p=Product.objects.filter(q1 & q2)
#     # print(p)
#     context={}
#     context['data']=p
    # return render(request,'product.html',context)

def catfilter(request, cv):
    # print(cv)
    q1 = Q(category=cv)  
    q2 = Q(is_active=True)

    p = Product.objects.filter(q1 & q2)
    # print(p)
    context = {'data': p}
    return render(request, 'product.html', context)

def sortfilter(request,sv):
    context={}
    # print(type(sv))
    if sv=='1':
        # p=Product.objects.order_by('-price')
        # context['data']=p
        t=('-price')
    else:
        # p=Product.objects.order_by('price')
        # context['data']=p
        t=('price')
    
    p=Product.objects.order_by(t).filter(is_active=True)
    context['data']=p
    return render(request,'product.html',context)

def pricefilter(request):
    mn=request.GET['min']
    mx=request.GET['max']

    # print(mn)
    # print(mx)
    q1=Q(price__gte= mn)
    q2=Q(price__lte= mx)
    q3=Q(is_active=True)

    p=Product.objects.filter(q1 &q2&q3)
    # print(p)
    context = {'data': p}
    return render(request,'product.html',context)

def product_detail(request,pid):
    p=Product.objects.filter(id=pid)
    # print(p)
    context = {'data': p}
    return render(request,'product_details.html',context)

def addtocart(request,pid):
    # print(pid)
    
    context={}
    if request.user.is_authenticated:
        print(request.user.id)
        u=User.objects.filter(id=request.user.id)
        # print(u)
        # print(u[0].email)
        p=Product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        
        if len(c)==1:
            context['errmsg']="Product Already Exist in Cart"
        else:    
            c=Cart.objects.create(pid=p[0],uid=u[0])
            c.save()
            context['success']='Product Added Successfully'
    
        context['data']=p
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')
    
def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    # print(c)
    s=0
    for i in c:
        s=s+i.pid.price*i.qty

    context={}
    context['data']=c
    context['total']=s
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    # print(c[0].qty)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1

    c.update(qty=q)
    return redirect('/cart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        a=i.pid.price*i.qty
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=a)
        o.save()
        i.delete()
    return redirect('/fetchorder')
    
def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={}
    s=0
    for i in o:
        s=s+i.amt
    context['data']=o
    context['total']=s
    context['n']=len(o)
    return render(request,'placeorder.html',context)

def srcfilter(request):
    s = request.GET.get('search', '').strip() 
    pname=Product.objects.filter(name__icontains=s)
    pdet=Product.objects.filter(pdetails__icontains=s)
    alldata=pname.union(pdet)
    # print(alldata)
    context={}
    if alldata.count()==0:
        context['errmsg']='Product Not Found'
    
    context['data']=alldata
    return render(request,'product.html',context)

import razorpay
def makepayment(request):
    
    client = razorpay.Client(auth=('rzp_test_0cZOKkv2JT3kMN', '2JknC0N7GWmm1I9Lj4R908AB'))
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt

    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data) 
    # print(payment)
    context={}
    context['payment']=payment

    return render(request,'pay.html',context)

# def paymentsuccess(request):

#     sub='Order confirm'
#     msg='Payment Successfull'
#     frm='yadavop97018@gmail.com'
#     u=User.objects.filter(id=request.user.id)
#     to=u[0].email

#     send_mail(
#         sub,
#         msg,
#         frm,
#         [to],
#         fail_silently=False
#     )

#     return render(request,'paymentsuccess.html')

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.models import User

def generate_invoice(user, total_amount):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Invoice Header
    p.drawString(100, 800, "Invoice")
    p.drawString(100, 780, f"Customer: {user.username}")
    p.drawString(100, 760, f"Email: {user.email}")
    p.drawString(100, 740, f"Total Amount Paid: ${total_amount}")  # ✅ Dynamic total price
    p.drawString(100, 720, "Thank you for shopping with us!")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


def paymentsuccess(request):
    subject = "Order Confirmation - Thank You for Shopping!"
    message = """Dear Customer,

Thank you for your purchase! Your payment was successful, and your order is confirmed.

We appreciate your business and look forward to serving you again.

Attached is your invoice for this transaction.

Best Regards,  
Your Store Team"""

    from_email = settings.DEFAULT_FROM_EMAIL
    user = User.objects.get(id=request.user.id)
    to_email = user.email

    # ✅ Calculate total amount from cart
    total_amount = sum(item.pid.price * item.qty for item in Cart.objects.filter(uid=user.id))

    # ✅ Generate Invoice with total amount
    invoice = generate_invoice(user, total_amount)

    # ✅ Send Email with Invoice Attachment
    email = EmailMessage(subject, message, from_email, [to_email])
    email.attach("Invoice.pdf", invoice.read(), "application/pdf")
    email.send()

    return render(request, "paymentsuccess.html", {"total": total_amount})
