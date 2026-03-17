# Archivo de rutas de productos
from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<str:pk>/', ProductDetailView.as_view(), name='product-detail'),
]