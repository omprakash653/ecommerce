from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'home.html')


def register(request):
    return render(request,'register.html')


def user_login(request):
    return render(request,'login.html')


from django.views import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt  # Only use if CSRF is causing issues
from .models import Contact
from django.contrib import messages

@method_decorator(csrf_exempt, name='dispatch')  # Apply decorator to all methods
class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        description = request.POST.get('description')

        # Save the data
        Contact.objects.create(name=name, contact=contact, email=email, description=description)

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # Redirect to success page


