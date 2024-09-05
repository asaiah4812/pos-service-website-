from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from datetime import date
import uuid
# from django_countries.fields import CountryField


User = get_user_model()
# Create your models here.

class Supplier(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='suppliers')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='categories')  # Foreign key to Company
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class Warehouse(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Dreamer_Warehouses'


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=225, unique=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website_url = models.URLField(null=True, blank=True)
    state = models.CharField(max_length=225)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Companies'

class CompanyAdministrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Foreign key to Company
    is_company_admin = models.BooleanField(default=True)  # Flag for company admin

    class Meta:
        unique_together = ('user', 'company')  # Ensure only one admin per company per user

    def __str__(self):
        return f"{self.user.email} - {self.company.company_name} Admin"

class Store(models.Model):
    STORE_STATUS = (
        ('Pending', 'pending'),
        ('Open', 'open'),
        ('Closed', 'closed')
    )
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    store_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    store_number = models.CharField(max_length=255)
    status = models.CharField(choices=STORE_STATUS, default='Pending', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return self.store_name

class Product(models.Model):
    name = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', default=1)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='suppliers', default=1)
    warehouse = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='warehouses')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    # manufacturing date
    mfdate = models.DateField(default=date.today)
    # expiring date
    expdate = models.DateField(default=date.today)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-added_at',)