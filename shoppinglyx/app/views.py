from django import forms
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext
from django.views import View
from . models import Customer, Product, OrderPlaced, Cart
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        buttomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category="L")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears': topwears, 'buttomwears': buttomwears, 'mobiles': mobiles, 'laptops':laptops, 'totalitem':totalitem})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {"product":product, "item_already_in_cart": item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        carts = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                return render(request, 'app/addtocart.html', {'carts': carts, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount

            data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        totalamount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
        data = {
            'amount': amount,
            'totalamount': totalamount
            }
        return JsonResponse(data)

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    orderplaced = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':orderplaced, 'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'Sony':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=1000)
    elif data == 'Above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=1000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem':totalitem})


def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Aachho' or data == 'Reebok' or data == 'Miaminx':
        topwears = Product.objects.filter(category='TW').filter(brand = data)
    elif data == 'Below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt = 1000)
    elif data == 'Above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
    return render(request, 'app/topwear.html', {'topwears': topwears})


def buttomwear(request, data=None):
    if data == None:
        buttomwear = Product.objects.filter(category='BW')
    elif data == 'Aachho' or data == 'Reebok' or data == 'Adidas':
        buttomwear = Product.objects.filter(category='BW').filter(brand = data)
    elif data == 'Below':
        buttomwear = Product.objects.filter(category='BW').filter(discounted_price__lt = 1000)
    elif data == 'Above':
        buttomwear = Product.objects.filter(category='BW').filter(discounted_price__gt = 1000)
    return render(request, 'app/buttomwear.html', {'buttomwear': buttomwear})

def laptop(request, data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'Alienware' or data == 'Asus':
        laptop = Product.objects.filter(category='L').filter(brand = data)
    elif data == 'Below':
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt = 1000)
    elif data == 'Above':
        laptop = Product.objects.filter(category='L').filter(discounted_price__gt = 1000)
    return render(request, 'app/laptop.html', {'laptop': laptop})


def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Account Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': address, 'totalamount': totalamount, 'cart_item':cart_item, 'totalitem':totalitem})

@login_required
def payment_done(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    custid = request.GET.get('custid')
    if custid == None:
        messages.info(request, "Please select any one Address")
        return redirect("checkout")
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totalitem = 0
    def get(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem':totalitem})
    
    def post(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Your profile is updated successfully')
        return render(request, 'app/profile.html', {'form': form, 'active':'btn-primary', 'totalitem':totalitem})