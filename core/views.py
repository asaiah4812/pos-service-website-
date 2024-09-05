from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from store.models import Company
from .models import Developer
# Create your views here.

User = get_user_model()
def home(request):
    company = Company.objects.first()
    developers = Developer.objects.all()
    context = {'company':company, 'developers':developers}
    return render(request, 'core/home.html', context)


def register_user(request):

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():  # Use the custom User model
                messages.warning(request, 'This email is already registered, Please use a different email.')
            else:
                form.save()
                messages.success(request, "Account created successfully. Please login to continue.")
                return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = RegisterForm()
    return render(request, 'core/signup.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
                
            login(request, user)
            messages.success(request, 'Login successfully')
            if hasattr(request.user, 'is_supplier') and request.user.is_supplier:
                return redirect('ordashboard')
            elif hasattr(request.user, 'is_buyer') and request.user.is_buyer:
                return redirect('ordashboard')
            else:
                return redirect('home')
        else:
            messages.warning(request, 'something went wrong')
            return redirect('login')
    else:
        return render(request, 'core/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has expired please login to continue')
    return redirect('login')
