from django.contrib.auth import login
from django.shortcuts import redirect,render
from .forms import SignUpForm

def signup(request):
    if request.user.is_authenticated: return redirect("core:home")
    form=SignUpForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        login(request,form.save()); return redirect("core:home")
    return render(request,"accounts/signup.html",{"form":form})
