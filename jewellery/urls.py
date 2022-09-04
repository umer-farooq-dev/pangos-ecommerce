from xml.etree.ElementInclude import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from online import views
from users import views as user_views
from users.forms import LoginForm, MyPasswordChangeForm
from users.views import account_verify, SignInView

admin.site.site_header = "Triiable Admin"
admin.site.site_title = "Triiable Admin Portal"
admin.site.index_title = "Welcome to Triiable Portal"

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('register/', user_views.register, name='register'),
                  path('registration/', user_views.CustomerRegistrationView.as_view(), name='customerregistration'),
                  path('accounts/login/',
                       SignInView.as_view(),
                       name='login'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('online/', include('online.urls')),
                  path("add-to-cart/", views.add_to_cart, name='add-to-cart'),
                  path("cart/", views.show_cart, name='showcart'),
                  path("pluscart/", views.plus_cart),
                  path("minuscart/", views.minus_cart),
                  path("removecart/", views.remove_cart),
                  path('checkout/', views.checkout, name='checkout'),
                  path('paymentdone/', views.payment_done, name='paymentdone'),
                  path('orders/', views.orders, name='orders'),
                  path('passwordchange/',
                       auth_views.PasswordChangeView.as_view(template_name='changepassword.html',
                                                             form_class=MyPasswordChangeForm,
                                                             success_url='/passwordchangedone/'),
                       name='passwordchange'),

                  path('passwordchangedone/',
                       auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'),
                       name='passwordchangedone'),
                  path('profile/', views.ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),
                  path('ring/', views.ring, name='ring'),
                  path('ring/<slug:data>', views.ring, name='ringdata'),
                  path('necklace/', views.necklace, name='necklace'),
                  path('necklace/<slug:data>', views.necklace, name='necklacedata'),
                  path('account-verify/<slug:token>', account_verify, name='account_verify'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
