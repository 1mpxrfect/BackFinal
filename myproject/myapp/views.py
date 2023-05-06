from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreateUserForm, ProductForm, SearchForm
from .models import Products, Category
import re
from django.contrib.auth.models import User


# Register
def sign_up(request):
    form = CreateUserForm()
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            messages.error(request, "Incorrect second password")
            return redirect("sign_up")
        elif User.objects.filter(username=uname).exists():
            messages.error(request, "This username already exists")
        elif len(pass1) < 8:
            messages.error(request, "Password should be min 8 simbols")
            return redirect("sign_up")
        elif not re.findall('[A-Z]', pass1):
            messages.error(request, "Password should be min one upper case")
            return redirect("sign_up")
        elif not re.findall('[@#$%!^&*]', pass1):
            messages.error(request, "Password should be min one special symbol")
            return redirect("sign_up")
        elif not re.findall('[a-z]', pass1):
            messages.error(request, "Password should be min one lower case")
            return redirect("sign_up")
        elif not re.findall('[0-9]', pass1):
            messages.error(request, "Password should be min one number")
            return redirect("sign_up")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('sign_in')

    context = {'f': form}

    return render(request, 'myapp/sign_up.html', context)


# Login
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            messages.info(request, 'Username or password incorrect')

    return render(request, 'myapp/sign_in.html')


# Log out
def log_out(request):
    logout(request)
    return redirect('sign_in')


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.uname = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        password = request.POST.get('password1')
        user.set_password(password)
        user.save()
        return redirect('/')

    context = {'user': user}
    return render(request, 'myapp/user.html', context)


# Site Admin
@login_required(login_url='sign_in')
def site_admin(request):

    products = Products.objects.all()
    total_products = products.count()

    users = User.objects.all()
    total_users = users.count()

    context = {
        'products': products,
        'total_products': total_products,
        'total_users': total_users
    }
    return render(request, 'myapp/site_admin.html', context)


# Create Product
def create_product(request):

    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('site_admin')

    context = {'f': form}
    return render(request, 'myapp/create_product.html', context)


# Update Product
def update_product(request, pk):

    product = Products.objects.get(id=pk)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            product.image = request.FILES['picture']
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        return redirect('admin')

    context = {'f': product}
    return render(request, 'myapp/edit_product.html', context)


# Delete Product
def delete_product(request, pk):

    product = Products.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('site_admin')

    context = {'product': product}
    return render(request, 'myapp/delete_product.html', context)


# Main Page
def main_page(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'myapp/main_page.html', context)


# Product detail
def product_detail(request, pk):
    product_details = get_object_or_404(Products, pk=pk)

    latest_comments = product_details.comment_set.order_by('-id')[:10]
    context = {'product_details': product_details, 'latest_comments': latest_comments}
    return render(request, 'myapp/product_detail.html', context)


def profile(request):
    return render(request, 'myapp/profile.html')


def create_user(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        user = User.objects.create_user(uname, email, pass1)
        user.save()
        return redirect('site_admin')

    return render(request, 'myapp/user.html')


def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.uname = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password1'))
        # user.is_staff = bool(request.POST.get('is_staff'))
        user.save()
        return redirect('site_admin')

    context = {'user': user}
    return render(request, 'myapp/user.html', context)


def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('site_admin')
    context = {'user': user}
    return render(request, 'myapp/delete_user.html', context)


def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'myapp/user_list.html', context)


def product_search(request):
    search_text = request.GET.get("search", "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    products = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        products = Products.objects.filter(name__icontains=search)
        if request.user.is_authenticated:
            search_history.append([search])
            request.session['search_history'] = search_history
    elif search_history:
        initial = dict(search=search_text)
        form = SearchForm(initial=initial)

    context = {"form": form, "search_text": search_text, "products": products}
    return render(request, "myapp/search_result.html", context)


def books(request):
    books = Products.objects.filter(category__name='Books')
    return render(request, 'myapp/books.html', {'books': books})


def games(request):
    games = Products.objects.filter(category__name='Games')
    return render(request, 'myapp/games.html', {'games': games})


def toys(request):
    toys = Products.objects.filter(category__name='Toys')
    return render(request, 'myapp/toys.html', {'toys': toys})


def sweets(request):
    sweets = Products.objects.filter(category__name='Sweets')
    return render(request, 'myapp/sweets.html', {'sweets': sweets})

