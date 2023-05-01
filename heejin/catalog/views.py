from django.shortcuts import render
from django.views import generic
from .engines import engines

# Create your views here.

from .models import Resin, Product, Client, Order
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import AddClientForm, AddResinForm, AddProductForm

from datetime import date, timedelta


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
        'machine_1': list(Order.objects.filter(order_date=date.today(), machine_num=1)),
        'machine_2': list(Order.objects.filter(order_date=date.today(), machine_num=2)),
        'machine_3': list(Order.objects.filter(order_date=date.today(), machine_num=3)),
        'machine_4': list(Order.objects.filter(order_date=date.today(), machine_num=4)),
        'machine_5': list(Order.objects.filter(order_date=date.today(), machine_num=5)),
        'machine_6': list(Order.objects.filter(order_date=date.today(), machine_num=6)),
        'machine_nums': [1,2,3,4,5,6]

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

def PrepareGraph(request):

    if request.method == "POST":
        
        products = []

        for k, v in request.POST.items():
            

            if v=="on":
                products.append(k)
        
        product_string = "+".join(products)
        date_string = "+".join([request.POST["start_date"], request.POST["end_date"]])
        date_product_string = date_string + "@&@" + product_string
        
        # Need to pass the start and end dates + products into the graph view. 
        # Combine the dates by + and products by +
        # 'date_string@&@product_string'

        

        return HttpResponseRedirect(reverse('graph', args=[date_product_string]))

    else:
        product_list = list(Product.objects.all())

        context = {
            "product_list": product_list,
        }
        
        return render(request, "catalog/prepare_graph.html", context)

def Graph(request, date_product_string):

    # products: The names of the product to graph.

    # Get relavent queryset of order objects. 
    # Calculate the labels [] for the x axis.
    # Calculate the datasets [dataset1, ...]. 
    # Dataset = {label: '', data: []}.
    # Display the graph. 

    [date_string, product_string] = date_product_string.split("@&@")

    datasets = []
    
    # [product1, product2, ...]
    product_l = product_string.split("+")
    product_objs = Product.objects.filter(product_name__in=product_l)

    # start_date & end_dates = ISOFORMAT start_date and end_date.
    [start_date, end_date] = date_string.split("+")
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)


    for product_obj in product_objs:

        # {'ISO': vol, ...}
        order_objs = Order.objects.filter(product__exact=Product.objects.get(product_name=product_obj.product_name), order_date__lte = end_date)
        volumes = engines.order2inventory_dictionary(order_objs, start_date, end_date)

        dataset = {}
        dataset['label'] = product_obj.product_name
        dataset['data'] = list(volumes)

        datasets.append(dataset)
            
    labels = []
    print(datasets)

    total_days = (end_date - start_date).days

    for x in range(total_days+1):
        labels.append(start_date + timedelta(days=x))


    context = {
        
        "labels": labels,
        "datasets": datasets
    }

    return render(request, 'catalog/graph.html', context)

def Schedule(request):

    if request.method == "POST":

        engines.schedule_order_input(request.POST)
        return HttpResponseRedirect(reverse('index'))
        
        
    else:
        obj = list(Product.objects.all())
        # form = ScheduleForm()
        context = {
            # "form": form,
            "product_list": obj
        }
        


    return render(request, "catalog/add_schedule.html", context)

def OrderFill(request, machine_num):

    if request.method == "POST":
        print(request.POST)
        engines.order_fill(request.POST)
        return HttpResponseRedirect(reverse('index'))

    else:
        date_today = engines.get_today_date()

        orders = list(Order.objects.all().filter(machine_num=machine_num, order_date=date_today))

        context = {
            "order_list": orders,
            "machine_num": machine_num,

        }
    return render(request, "catalog/order_fill.html", context)

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
