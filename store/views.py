from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company,CompanyAdministrator, Store, Category, Supplier, Buyer, Product
from .forms import CompanyForm, StoreForm, UpdateStoreForm,  CategoryForm,   UpdateCategory, SupplierForm, BuyerForm
from .permissions import verified_user_only
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()
# Create your views here.
@verified_user_only
@login_required
def dashboard(request):
    user = request.user
    try:
       company_admin = CompanyAdministrator.objects.get(user=user)
    except CompanyAdministrator.DoesNotExist:
        messages.warning(request, 'You are not authorized to access this dashboard.')
      # User is not a company administrator, redirect or raise an error
        return redirect('home')
    stores = Store.objects.filter(manager=request.user)
    store_total = stores.count()
    suppliers = Supplier.objects.filter(company=request.user.company)
    supplier_total = suppliers.count()
    buyers = Buyer.objects.filter(company=request.user.company)
    buyer_total = buyers.count()
    company = company_admin.company
    context =  {'company':company, 'store_total':store_total, 'supplier_total':supplier_total, 'buyer_total':buyer_total}
    return render(request, 'core/dashboard.html', context)
@login_required
def ordashboard(request):
    try:
        company = request.user.buyer.company
        products = Product.objects.filter(company=company)
        product_count = products.count()
        context = {
            'product_count':product_count,
            
        }
    except ObjectDoesNotExist:
        messages.warning(request, 'User not authorised')
        return redirect('home')
    return render(request, 'core/ordashboard.html', context)


@verified_user_only
@login_required
def stores(request):
    stores = Store.objects.filter(manager=request.user)
    form = StoreForm()
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.manager = request.user
            store.save()
            messages.success(request, 'Your store has been created successfully')
            return redirect('stores')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = StoreForm()
    context = {
        'form':form,
        'stores':stores
    }
    return render(request, 'store/stores.html', context)

@verified_user_only
@login_required
def update_store(request, pk):
    store = Store.objects.get(pk=pk)
    if request.method == 'POST':
        edit_form = UpdateStoreForm(request.POST, instance=store)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Your Store has been updated successfully')
            return redirect('stores')
        else:
            messages.error(request, 'something went wrong')
            return redirect('stores')
    else:
        edit_form = UpdateStoreForm(instance=store)
        context = {'edit_form':edit_form, 'store':store}
    return render(request, 'partials/store_form.html', context)


@verified_user_only
@login_required
def delete_store(request, pk):
    store = Store.objects.get(id=pk)
    store.delete()
    return redirect('stores')

@verified_user_only
@login_required
def categories(request):
    categories = Category.objects.filter()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.company = request.user.company
            comp.save()
            messages.success(request, "Category created successfully 🙌")
            return redirect('categories')
        else:
            messages.error(request, 'something went wrong my guy')
            return redirect('categories')
    else:
        form = CategoryForm()
    context = {
        "categories":categories,
        'form':form
    }
    return render(request, 'store/categories.html', context)



@verified_user_only
@login_required
def update_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        update_form = UpdateCategory(request.POST, instance=category)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Category Updated successfully')
            return redirect('categories')
        else:
            messages.error(request, 'something went wrong')
            return redirect('categories')
    else:
        update_form = UpdateCategory(instance=category)

    context = {
        'category':category,
        'update_form':update_form
    }
    return render(request, 'partials/category_form.html', context)

@login_required
@verified_user_only

def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect('categories')


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            print(form)
            messages.success(request, 'Your Company Has been Created Successfull')
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = CompanyForm()
    return render(request, 'store/create_company.html', {'form':form})


# create supplier view funtion
@login_required
@verified_user_only
def suppliers(request):
    suppliers = Supplier.objects.filter(company=request.user.company)
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                user = User.objects.create_user(email=email, username=username, password=password, is_supplier=True)
                Supplier.objects.create(user=user, name=name, address=address, company=request.user.company)
                messages.success(request, 'Supplier created successfully')
                return redirect('suppliers')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('suppliers')
        else:
            messages.warning(request, 'invalid form details')
            return redirect('suppliers')
    else:
        form = SupplierForm()
    context = {
        'form':form,
        'suppliers':suppliers
    }
    return render(request, 'store/suppliers.html', context)    


@login_required
@verified_user_only
def buyers(request):
    buyers = Buyer.objects.filter(company=request.user.company)
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                user = User.objects.create_user(email=email, username=username, password=password, is_buyer=True)
                Buyer.objects.create(user=user, name=name, address=address, company=request.user.company)
                messages.success(request, 'Buyer created successfully')
                return redirect('buyers')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists. Please use a different email.')
                return redirect('buyers')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('buyers')
        else:
            messages.success(request, 'invalid form field')
    else:
        form = BuyerForm()
    context = {'buyers':buyers, 'form':form}
    return render(request, 'store/buyers.html', context)