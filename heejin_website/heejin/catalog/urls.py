from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resins/', views.ResinListView.as_view(), name='resins'),
    path('resins/<str:pk>', views.ResinDetailView.as_view(), name='resin-detail'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<str:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('add_client/', views.AddClient, name='add-client'),


]
