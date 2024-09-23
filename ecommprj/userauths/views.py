from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

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