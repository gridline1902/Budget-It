from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


# Create your views here.
def register(request):
    # if request made on register webpage is to post
    if request.method == "POST":
        # create an object for NewUserForm and pass in request method
        form = RegisterForm(request.POST)
        # check if all attributes of form is valid
        if form.is_valid():
            # form is saved to user object
            user = form.save()
            # gets username from form
            username = form.cleaned_data.get('username')
            messages.success(request=request, message=f"New Account Created: {username}")
            # makes request to login as user
            login(request=request, user=user)
            messages.info(request=request, message=f"You are now logged in as {username}")
            # redirects to homeview page
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    # saves NewUserForm to object
    form = RegisterForm()
    # returns render view for register template
    return render(request=request,
                  template_name="Register/register.html",
                  context={"form": form})
    
def logout_request(request):
    # makes logout request to logout
    logout(request)
    messages.info(request, "Logged Out Successfully")
    # redirect to landing page
    return redirect("/")



def login_request(request):
    if request.method == "POST":
        # object for Authenticationform is created
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            # gets username and password and saves to objects
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # use authenticate method to authenticate user
            user = authenticate(username=username, password=password)
            # checks if user exists
            if user is not None:
                # login if user exists
                login(request, user)
                messages.info(request=request, message=f"You are now logged in as {username}")
                # redirects to homeview template page
                return redirect("/")
            else:
                messages.error(request, "Invalid Username or Password")
        # else if user doesn't exist don't authenticate
        else:
            messages.error(request, "Invalid Username or Password")
    # saves AuthenticationForm to object
    form = AuthenticationForm()
    # return template view
    return render(request, "Registration/login.html",
                  {"form": form, "messages": messages.get_messages(request)})