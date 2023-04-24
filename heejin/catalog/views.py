from django.shortcuts import render
from django.views import generic
from .engines import engines

# Create your views here.

from .models import Resin, Product, Client, Order
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import AddClientForm, AddResinForm, AddProductForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_resins = Resin.objects.all().count() 
    num_clients = Client.objects.all().count()
    num_products = Product.objects.all().count()
    num_orders = Order.objects.all().count()

    context = {
        'num_resins': num_resins,
        'num_clients': num_clients,
        'num_products': num_products,
        'num_orders': num_orders,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def AddClient(request):

    if request.method == "POST":

        form = AddClientForm(request.POST, request.FILES)

        if form.is_valid():
            
            engines.client_csv_to_input(request.FILES['client_names_file'])
            return HttpResponseRedirect(reverse('clients'))
        
        
    else:
        form = AddClientForm()

        context = {
            'form': form
        }

    return render(request, 'catalog/add_client.html', context)

def AddResin(request):

    if request.method == "POST":

        form = AddResinForm(request.POST, request.FILES)

        if form.is_valid():
            engines.resin_csv_to_input(request.FILES['resin_file'])
            return HttpResponseRedirect(reverse('resins'))
    
    else:
        form = AddResinForm()

        context = { 
            'form': form
        }

    return render(request, 'catalog/add_resin.html', context)

def AddProduct(request):

    if request.method == "POST":

        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            engines.product_csv_to_input(request.FILES['product_file'])
            return HttpResponseRedirect(reverse('products'))

        context = {
            "form": form
        }
        return render(request, 'catalog/test.html', context=context)
    
    else:

        form = AddProductForm()

        context = { 
            'form': form
        }

        return render(request, 'catalog/add_product.html', context=context)

def Graph(request):

    # Get relavent queryset of order objects. 
    # Calculate the inventory json file. 
    # Display the graph. 


    objs = list(Order.objects.all().filter(product='X150 FRT W-ARCH-LH'))
    print(objs)


    data = engines.order2inventory_dictionary(objs)
    print(list(Order.objects.all())[0].product)
    print(objs)
    print(data)


    context = {
        'data_1': data
    }

    return render(request, 'catalog/graph.html', context)

class ResinListView(generic.ListView):
    model = Resin
    
class ResinDetailView(generic.DetailView):
    model = Resin

class ProductListView(generic.ListView):
    model = Product

class ProductDetailView(generic.DetailView):
    model = Product

class ClientListView(generic.ListView):
    model = Client
