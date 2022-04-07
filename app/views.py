from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import NewUserForm
from django.contrib.auth.models import User
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
        password = request.POST['password1']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [userid])
            account = cursor.fetchone()
            if account is not None:
                user = NewUserForm(account)
                login_user = user.save()
                login(request, login_user)
                username = user.userid
                return render(request, 'app/profile.html', {'users':username})
            else:
                messages.success(request, ("there was an error logging in, please try again."))
                return redirect('login')
    return render(request, 'app/login.html', {})
    
def signin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, You logged in to {user.username}')
                return redirect('register')
            else:
                messages.error(request, ("Invalid username or password. 1"))
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM allusers WHERE userid = %s", [username])
                account = cursor.fetchone()
                if account[2] == password:
                    user = NewUserForm(account[0], account[1], account[2], account[2])
                    login_user = user.save()
                    login(request, login_user)
                    username = user.userid
                    return render(request, 'app/profile.html', {'users':username})
                else:
                    messages.success(request, f'Invalid, You logged in to password {account[2]}')
    form = AuthenticationForm()
    return render(request,
                    "app/login.html",
                    context={"form":form})
"""
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, You logged in to {user.username}')
            return redirect('home')
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM allusers WHERE userid = %s", [username])
                account = cursor.fetchone()
                if account[2] == password:
                    created = User.objects.create_user(username, str(account[1]), password)
                    #created = NewUserForm(username, str(account[1]), password, password)
                    #created = UserCreationForm(account)
                    #user = NewUserForm(created)
                    #login_user = created.save()
                    login(request, created)
                    messages.success(request, f'Welcome, You logged in to {username}')
                    return redirect('home')
                else:
                    messages.success(request, f'Invalid, You logged in to password {account[2]}')
            messages.success(request, f'{username} {password}')	
            return redirect('login')	


    else:
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
        cursor.execute("SELECT * FROM transactions WHERE b_id =%s", [id])
        trans = cursor.fetchall()
        cursor.execute("SELECT * FROM products WHERE sellerid =%s", [id])
        list = cursor.fetchall()

    result_dict = {'user': user}

    return render(request, 'app/profile.html', {'user': user, 'list':list, 'trans':trans})


def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid = %s", [id])
        customer = cursor.fetchone()
        cursor.execute("SELECT SUM(qty) FROM transactions WHERE p_id = %s", [id])
        order = cursor.fetchone()
        if order is None:
            order = 0
	
    #result_dict = {'cust': customer}

    return render(request,'app/view.html',{'cust':customer, 'order':order})

def search_products(request):
    qns = request.POST['searched']
    qns = "%" + qns + "%"
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE lower(name) LIKE lower(%s)", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_products.html', {'searched': searched, 'qns':qns})

def search_users(request):
    qns = request.POST['searched']
    qns = "%" + qns + "%"
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE lower(userid) LIKE lower(%s)", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_users.html', result_dict)

def purchase(request):
    deliver = request.GET['delivery']
    b_id = request.user.username
    s_id = request.GET['s_id']
    p_id = request.GET['p_id']
    qty = request.GET['qty']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO transactions(b_id, s_id, p_id, qty, delivery, status) VALUES (%s, %s, %s, %s, %s, %s)"
                , [b_id, s_id, p_id, qty, deliver, "pending"])
        cursor.execute("SELECT * FROM products WHERE productid = %s", [p_id])
        customer = cursor.fetchone()
        cursor.execute("SELECT SUM(qty) FROM transactions WHERE p_id = %s", [p_id])
        order = cursor.fetchone()
        messages.success(request, f'You bought {qty}x of this item.')
        return render(request, 'app/view.html', {'cust':customer, 'order':order})

def sort_top(request):
    qns = request.GET['qns']
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.productid, p.sellerid, p.name, p.description, p.price, p.category, p.allergen, p.minorder FROM products p LEFT OUTER JOIN transactions t ON p.productid =t.p_id WHERE lower(p.name) LIKE lower(%s) GROUP BY p.productid ORDER BY coalesce(sum(t.qty),0) DESC", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_products.html', {'searched': searched, 'qns':qns})

def sort_priceup(request):
    qns = request.GET['qns']
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.productid, p.sellerid, p.name, p.description, p.price, p.category, p.allergen, p.minorder FROM products p LEFT OUTER JOIN transactions t ON p.productid =t.p_id WHERE lower(p.name) LIKE lower(%s) GROUP BY p.productid ORDER BY p.price;", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_products.html', {'searched': searched, 'qns':qns})

def sort_pricedown(request):
    qns = request.GET['qns']
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.productid, p.sellerid, p.name, p.description, p.price, p.category, p.allergen, p.minorder FROM products p LEFT OUTER JOIN transactions t ON p.productid =t.p_id WHERE lower(p.name) LIKE lower(%s) GROUP BY p.productid ORDER BY p.price DESC;", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_products.html', {'searched': searched, 'qns':qns})

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
