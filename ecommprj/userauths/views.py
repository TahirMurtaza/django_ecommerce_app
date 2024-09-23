from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauths.models import User

# Create your views here.
def register_view(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            form_data = form.cleaned_data
            username = form_data["username"]
            messages.success(request, f"Hey {username}! your account was created successfully.")
            new_user = authenticate(username=form_data["email"], 
                                    password=form_data["password1"])
            login(request,new_user)
            return redirect("core:index")
    context = {'form': form}
    return render(request, "userauths/sign-up.html",context)  

def login_view(request):
    if request.user.is_authenticated:
        messages.warning("You already logged in.")
        return redirect('core:index')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email,password=password)
            if user:
                login(request,user)
                messages.success(request,"You are logged in.")
            else:
                messages.warning(request,"You are not registered. Please create new account.")
            return redirect('core:index')
        except:
            messages.warning(request,f"User with {email} doesn't exist.")
            
        
    context = {}
    return render(request, "userauths/sign-in.html",context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out.")       
    return redirect('userauths:sign-in')

