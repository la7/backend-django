from django.urls import path
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    # Rutas para /api/users/
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<str:pk>/', UserDetailView.as_view(), name='user-detail'),
]