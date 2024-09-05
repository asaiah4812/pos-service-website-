from django.contrib import admin
from . models import Company, CompanyAdministrator, Store, Category, Supplier, Buyer, Product, Warehouse

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone', 'email', 'country', 'state']

admin.site.register(CompanyAdministrator)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'location', 'store_number', 'status']

admin.site.register(Category)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'company']

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'company']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost_price', 'company', 'supplier', 'warehouse', 'selling_price', 'quantity']
    list_editable = ['cost_price', 'selling_price', 'company', 'supplier', 'warehouse', 'quantity']
    list_filter = ['company', 'supplier', 'warehouse']
