import json
import uuid
from email import message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt

import users
from users.forms import CustomerProfileForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def send_email(email):
    send_mail(
        'Verify Email',
        f'Hi: Your Order Successfully Placed',
        'ibsoft0786@gmail.com',
        ['ufkeyfans786@gmail.com'],
        fail_silently=False,
        # subject="Verify Email",
        # message=f'Hi Click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}',
        # from_email=settings.EMAIL_HOST_USER,
        # recipient_list=[email],
        # fail_silently=False,
    )


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 30.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount

    email_v = VerifiedEmail(user=user)

    send_email(user.email)

    return render(request, 'checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


def get_context_data(self, **kwargs):
    product = Product.objects.get(name="Test Product")
    context = super(checkout, self).get_context_data(**kwargs)
    context.update({
        "product": product,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    })
    return context


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': add, 'active': 'btn-primary'})


def contactUs(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
    return render(request, 'contact.html')


def productReport(request):
    if request.method == "POST":
        select_report = request.POST.get('select_report', '')
        product_name = request.POST.get('product_name', '')
        user_email = request.POST.get('user_email', '')
        report_message = request.POST.get('report_message', '')
        report = ProductReport(select_report=select_report, product_name=product_name, user_email=user_email,
                               report_message=report_message)
        report.save()

    return render(request, 'productreport.html')


@login_required
def trackingSystem(request):
    return render(request, 'orders.html')


def search(request):
    return render(request, 'search.html')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        ring = Product.objects.filter(category='R')
        bracelet = Product.objects.filter(category='B')
        necklace = Product.objects.filter(category='N')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'index.html',
                      {'ring': ring, 'bracelet': bracelet, 'necklace': necklace, 'totalitem': totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'itemViews.html',
                      {'product': product, 'totalitem': totalitem, 'item_already_in_cart': item_already_in_cart})


@login_required
def add_to_cart(request):
    totalitem = 0;
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    Cart(user=user, product=product).save()
    return redirect('/cart', {'totalitem': totalitem})


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 30.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request, 'addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount})
        else:
            return render(request, 'emtycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 30.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 30.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 30.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'users/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            address1 = form.cleaned_data['address1']
            address2 = form.cleaned_data['address2']
            city = form.cleaned_data['city']
            postcode = form.cleaned_data['Postcode']
            reg = Customer(user=usr, name=name, address1=address1, address2=address2, city=city, Postcode=postcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
            return render(request, 'users/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'order_placed': op})


def ring(request, data=None):
    if data == None:
        ring = Product.objects.filter(category='R')
    elif data == 'Gold' or data == 'Silver' or data == 'Dia':
        ring = Product.objects.filter(category='R').filter(brand=data)

    return render(request, 'ring.html', {'ring': ring})


def necklace(request, data=None):
    if data == None:
        necklace = Product.objects.filter(category='N')
    elif data == 'Gold' or data == 'Silver' or data == 'Dia':
        necklace = Product.objects.filter(category='N').filter(brand=data)

    return render(request, 'neclace.html', {'necklace': necklace})


import stripe
from django.conf import settings
from django.views import View

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutSession(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.selling_price,
                        'product_data': {
                            'name': product.title,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


def PaymentSuccess(request):
    context = {
        'payment_status': 'success',
    }
    return render(request, "orders.html", context)


def PaymentCancel(request):
    context = {
        'payment_status': 'cancel',
    }
    return render(request, "orders.html", context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="ibsoft0786@gmail.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})