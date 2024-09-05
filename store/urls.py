from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('core/', views.ordashboard, name='ordashboard'),
    path('create-company/', views.create_company, name='create_company'),
    path('stores/', views.stores, name="stores"),
    path('categories/', views.categories, name="categories"),
    path('update-category/<int:pk>/', views.update_category, name="update_category"),
    path('delete-category/<int:pk>/', views.delete_category, name="delete_category"),
    path('update-store/<int:pk>/', views.update_store, name="update_store"),
    path('delete-store/<int:pk>/', views.delete_store, name="delete_store"),
    path('suppliers/', views.suppliers, name="suppliers"),
    path('buyers/', views.buyers, name="buyers")
]
