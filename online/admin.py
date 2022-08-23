from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(OrderPlaced)
admin.site.register(ProductReport)


@admin.register(VerifiedEmail)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'user', 'verify']
