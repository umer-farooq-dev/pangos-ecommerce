from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from online import views
from online.views import *

urlpatterns = [
    path("", views.ProductView.as_view(), name="OnlineHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contactUs, name="ContactUs"),
    path("report/", views.productReport, name="report"),
    path("tracker/", views.trackingSystem, name="TrackingSystem"),
    path("search/", views.search, name="Search"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path("checkout/", views.checkout, name="Checkout"),
    path("create-checkout-session/", CheckoutSession.as_view(), name="create-checkout-session"),
    # path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    # path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path("payment-success", PaymentSuccess, name="payment-success"),
    path("payment-cancel", PaymentCancel, name="payment-cancel"),
]
