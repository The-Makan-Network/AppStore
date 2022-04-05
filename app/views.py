from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
#from models import useraccounts

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

    if request.POST:
        form = NewUserForm(request.POST)
        ## Check if userid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [request.POST['username']])
            user = cursor.fetchone()
            ## No customer with same id
            if not form.is_valid():
                messages.success(request, ("Password does not pass requirements. Please try again."))
                return redirect('register')
            elif form.is_valid() and user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO allusers(userid, phoneno, password) VALUES (%s, %s, %s)"
                        , [request.POST['username'], request.POST['phoneno'], request.POST['password1'] ])
                newuser = form.save()
                login(request, newuser)
                messages.success(request, ("Registration successful. Welcome, {username}!"))
                return redirect('home')
            else:
                messages.success(request, ("Username or Phone Number already taken. Please Try Again."))
                return redirect('register')
		
    form = NewUserForm()
    return render(request, "app/register.html", {})
"""
def signin(request):
    if request.POST:
	userid = request.POST['username']
        with connection.cursor as cursor:
            login_check = cursor.execute("SELECT * FROM allusers WHERE userid = %s", [username])
            if login_check:
                if login_check.password == request.POST['password']

"""
def signin(request):
    if request.POST:
        userid = request.POST['username']
        password = request.POST['password1']
        with connection.cursor as cursor:
            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [userid])
            account = cursor.fetchone()
            if account is not None:
                login(request, account)
                username = account.userid
                return render(request, 'app/profile.html', {'users':username})
            else:
                messages.success(request, ("there was an error logging in, please try again."))
                return redirect('login')
    return render(request, 'app/login.html', {})	

def signout(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('home')

		
def profile(request, id):
    """Shows the main page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE userid =  %s",[id])
        user = cursor.fetchone()

    result_dict = {'user': user}

    return render(request, 'app/profile.html', result_dict)


def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

def search(request, qns):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from allusers u, products p WHERE u.userid LIKE '%s%' OR p.name LIKE '%s%'", [qns])
        searched = cursor.fetchall()
    result_dict = {'qns': searched}

    return render(request, 'app/search.html', result_dict)


"""
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You are now logged in as {username}"))
                return redirect('register')
            else:
                messages.error(request, ("Invalid username or password."))
        else:
            messages.success(request, ("Invalid username or password."))
    form = AuthenticationForm()
    return render(request,
                    "app/login.html",
                    context={"form":form})

"""
"""
def signin(request):

    if request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=username, password1=password1)
        if user is not None:
            login(request, user)
            return redirect('register')
        else:
             messages.success(request, ("Invalid UserID or Password. Try Again."))
             return redirect('login')

    return render(request, 'app/login.html', {})
    
"""
