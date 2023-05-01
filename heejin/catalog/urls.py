from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resins/', views.ResinListView.as_view(), name='resins'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('add_client/', views.AddClient, name='add-client'),
    path('add_product/', views.AddProduct, name='add-product'),
    path('add_resin/', views.AddResin, name='add-resin'),
    path('prepare_graph/', views.PrepareGraph, name="prepare-graph"),
    path('graph/<str:date_product_string>/', views.Graph, name='graph'),
    path('schedule/', views.Schedule, name='schedule'),
    path('order_fill/<int:machine_num>/', views.OrderFill, name='order-fill'),


]
