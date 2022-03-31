from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm

# Create your views here.
def home(request):

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products ORDER BY productid")
        products = cursor.fetchall()

    result_dict = {'products': products}

    return render(request, 'app/home.html', result_dict)


# Create your views here.
def register(request):
    context = {}
    status = ''

    if request.POST:
        form = NewUserForm(request.POST)
        ## Check if userid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [request.POST['username']])
            user = cursor.fetchone()
            ## No customer with same id
            if user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO allusers(userid, phoneno, password) VALUES (%s, %s, %s)"
                        , [request.POST['username'], request.POST['phoneno'], request.POST['password1'] ])
                newuser = form.save()
                login(request, newuser)
                messages.success(request, f"Registration successful. Welcome, {username}!")
                return redirect('/')    
            else:
                status = 'User with ID %s already exists' % (request.POST['username'])
		
    form = NewUserForm()
    context['status'] = status
 
    return render(request, "app/register.html", context)

def signin(request):
    context = {}
    status = ''

    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password1=password1)
            if user is not None:
                login(request, user)
                return redirect('register')
            else:
                messages.success(request, ("Invalid UserID or Password. Try Again."))
                return redirect('login')

    return render(request, 'app/login.html', {})
		
def profile(request, id):
    """Shows the main page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE userid =  %s",[id])
        user = cursor.fetchone()

    result_dict = {'users': users}

    return render(request, 'app/profile.html', result_dict)


def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)
