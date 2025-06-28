from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ImageForm
from .models import Image
# Create your views here.
def home(req):
    if req.method == 'POST':
        form = ImageForm(req.POST, req.FILES) # Create an instance of ImageForm with POST data and files.
        # If the form is valid, save the data to the database.
        if form.is_valid():
            form.save()
    form = ImageForm() # Create a new instance of ImageForm for the empty form.
    img = Image.objects.all() # Fetch all Image objects from the database.
    return render(req, 'home/home.html', {'img':img, 'form': form}) 


def login_view(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, 'Invalid username or password!')
            return redirect('login')
    
    return render(req, 'home/login.html')


def signup(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        pass1 = req.POST.get('password1')
        pass2 = req.POST.get('password2')

        if pass1 != pass2:
            messages.error(req, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(req, 'Username already taken!')
            return redirect('signup')

        my_user = User.objects.create_user(username=username, email=email, password=pass1)
        my_user.save()
        messages.success(req, 'Account created successfully!')
        return redirect('login')
    
    return render(req, 'home/signup.html')

def logout_view(req):
    logout(req)
    messages.success(req, 'Logged out successfully!')
    return redirect('login')