from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def index(request, id):
    # get the object based on the id
    ls = ToDoList.objects.get(id=id)   
    # checks if ToDoList objects exists for specific user
    if ls in request.user.todolist.all():
        # {"save": ["save"], "c1":["clicked"]}
        # ......if we click the save button in the form, the name of button points to the value of button
        if request.method == 'POST':
            print(request.POST)
        # handles the request if "save" button is clicked
            if request.POST.get("save"):
        # loops through all the items in the ToDoList
                for item in ls.item_set.all():
        # handles the request if "checked" button is clicked
                    if request.POST.get("c" + str(item.id)) == "clicked":
        # sets the status of the item_checkbox to "checked"
                        item.complete = True
                    else:
        # sets the status of the item_checkbox to "unchecked"
                        item.complete = False
        # saves the item object
                    item.save()
        # this elif statement handles the request if "add new item" button is clicked
            elif request.POST.get("newItem"):
        # we then get the text from input field with name "new"
                txt = request.POST.get("new")
        # perform validation of the txt object
                if len(txt) > 2:
        # we then create a new item object and save it
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("Please enter more than 2 characters")
        return render(request, "Home/list.html", {"ls": ls})
    # item = ls.item_set.get(id=1)
    return render(request, "Home/view.html", {})
    # return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" %(ls.name, str(item.text)))


def landing_page(request):
    return render(request, "Home/Landing_Page.html", {})


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
            
        return HttpResponseRedirect("/%i" %t.id)

    else:
    # creates an instance of the form
        form = CreateNewList()
    return render(request, "Home/create.html", {"form": form})


def view(request):
    return render(request, "Home/view.html", {})
