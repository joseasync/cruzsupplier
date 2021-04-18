from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import OrderForm, CreateUserForm



def registerPage(request):
    form = CreateUserForm() #Authentication do django

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado!!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) #loga o user...
            return redirect('home') #django method auth


    context = {}
    return render(request, 'accounts/login.html', context)

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers
    ,'total_orders': total_orders, 'total_customers': total_customers
    , 'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


def products(request):   
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk_customer):
    customer = Customer.objects.get(id=pk_customer)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {'customer': customer, 'orders': orders, 'total_orders' : total_orders}
    return render(request, 'accounts/customer.html', context)


def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        # print('Print Post', request.POST)
        form = OrderForm(request.POST) # O orderFOrm vai gerenciar isso pra gente....
        #Se o form tiver show, ele salva o dado no db
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form }
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
   
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) #preenche a instancia.
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # Utiliza a instancia do order pra poder atualizar... 
        if form.is_valid():
            form.save()
            return redirect('/')


    context = { 'form': form, }
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')


    context = { 'item': order }
    return render(request, 'accounts/delete.html', context)