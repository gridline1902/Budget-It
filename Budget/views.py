from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.


def landing_page(request):
    return render(request, "Home/Landing_Page.html", {})


def index(request, name):
    # get the object based on the id
    ls = ToDoList.objects.get(name=name)   
    # checks if ToDoList objects exists for specific user
    if ls in request.user.todolist.all():
        if request.method == "POST":
            if request.POST.get("calculate"):
                amount = request.POST.get("amount")
                try:
                    # create a new item and calculate needs, wants, and savings
                    item = ls.item_set.create(amount=float(amount))
                    needs = float(amount) * 0.5
                    wants = float(amount) * 0.3
                    savings = float(amount) * 0.2
                    item.needs = needs
                    item.wants = wants
                    item.savings = savings
                    item.save()
                except ValueError:
                    print("Please enter a valid amount")
            # check if the delete button was pressed
            elif "item_id" in request.POST:
                item_id = request.POST.get("item_id")
                try:
                    # get the item and delete it
                    item = ls.item_set.get(id=item_id)
                    item.delete()
                except Item.DoesNotExist:
                    print("Item does not exist")
            else:
                print("Not Clicked")      
        # render the list.html template with the to-do list object
        return render(request, "Home/list.html", {"ls": ls})
    # render the view.html template if the to-do list object doesn't exist
    return render(request, "Home/view.html", {})


def create(request):
    # checks if you posting data to server
    if request.method == "POST":  
    # holds all the form data in a dictionary
        form = CreateNewList(request.POST)
    # checks if the form is valid
        if form.is_valid():
    # gets the cleaned data from the form
            n = form.cleaned_data["name"]
    # we then create a new ToDoList object with the above cleaned_data
            t = ToDoList(name=n)
    # saves the object to the databasew
            t.save()
    # for saving a ToDoList to the specific user now
            request.user.todolist.add(t)
            
        return HttpResponseRedirect("/%s" %t.name)

    else:
    # creates an instance of the form
        form = CreateNewList()
    return render(request, "Home/create.html", {"form": form})


def view(request):
    if request.user.is_authenticated:
        # Get all to-do lists for the current user
        todolists = request.user.todolist.all()
        if not todolists:
            # If the user has no to-do lists, redirect to the home page
            return redirect("/create/")
        else:
            # Render the view template with the to-do lists
            return render(request, "Home/view.html", {})
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect("/login/")

def about(request):
    return render(request, "Home/about_us.html", {})

def services(request):
    return render(request, "Home/services.html", {})

def delete_todo_list(request, name):
    # Get the to-do list object based on the name
    todo_list = ToDoList.objects.get(name=name)

    # Check if the user has permission to delete this to-do list
    if todo_list in request.user.todolist.all():
        # Delete the to-do list object
        todo_list.delete()
        # Redirect the user to the view page
        return redirect("/view/")
    else:
        # Return an error message
        return HttpResponse("You do not have permission to delete this to-do list.")