from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Resin, Product, Client, Order
from catalog.forms import AddClientForm, AddResinForm, AddProductForm

from datetime import date
from .helper_data import data_helpers
from .helper_graph import graph_helpers
from .helper_inventory import inventory_helpers



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

            if request.POST['client_names_file'] != '':

                data_helpers.client_csv_to_input(request.FILES['client_names_file'])

            else:
                data_helpers.add_client(request.POST)
            
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

            if request.POST['resin_file'] != '':
                data_helpers.resin_csv_to_input(request.FILES['resin_file'])
            
            else:
                data_helpers.add_resin(request.POST)
            
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

            if request.POST['product_file'] != '':
                data_helpers.product_csv_to_input(request.FILES['product_file'])
            
            else:
                data_helpers.add_product(request.POST)
                
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
    # 그래프 준비물 받기위한 뷰

    if request.method == "POST":
        
        products = []

        for k, v in request.POST.items():
            if v=="on":
                products.append(k)

        date_product_string = graph_helpers.date_product_string_encoder(request.POST["start_date"], 
                                                                 request.POST["end_date"], 
                                                                 products)

        return HttpResponseRedirect(reverse('graph', args=[date_product_string]))

    else:
        product_list = list(Product.objects.all())

        context = {
            "product_list": product_list,
        }
        
        return render(request, "catalog/prepare_graph.html", context)

def Graph(request, date_product_string):

    # 그래프 그리는 뷰.

    # output: 
    # 1. labels = [시작 날짜, date2, date3..., 끝날짜] Chart.js이 필요한 data
    # 2. datasets = [dataset1, dataset2,...]
    # dataset = {label: '', data: []}
    # https://www.chartjs.org/docs/latest/general/data-structures.html

    #Initialize variables
    # start_date: 그래프할 첮 날짜
    # end_date: 그래프할 첮 날짜
    # product_list: 그래프할 제품 list
    start_date, end_date, product_l = graph_helpers.date_product_string_decoder(date_product_string)

    
    # datasets
    datasets = []
    product_objs = Product.objects.filter(product_name__in=product_l)
    for product_obj in product_objs:
        order_objs = Order.objects.filter(product__exact=Product.objects.get(product_name=product_obj.product_name), 
                                          order_date__lte = end_date)
        order_volume_list = inventory_helpers.order_qlist2order_volume(order_objs)

        if len(order_volume_list) > 0:

            # Initialise variables
            inventory = {}
            first_order = order_volume_list[0]
            first_order_date = first_order[0]

            # Setup inventory, order_volume_list
            inventory = inventory_helpers.setup_inventory_dict(inventory, first_order)
            order_volume_list.pop(0)

            # Get inventory for product
            inventory = inventory_helpers.volume_list2inventory_dict(order_volume_list, inventory)

            # Get graph inventory for product
            graph_inventory = {}
            graph_inventory = graph_helpers.inventory_dict2graph_inventory_dict(inventory, graph_inventory,
                                                              start_date, end_date,
                                                              first_order_date)

        else:
            # No orders for product

            # Get graph_inventory of 0s.
            graph_inventory = {}
            graph_inventory = graph_helpers.empty_inventory_dict2graph_inventory_dict(graph_inventory, start_date, end_date)


        # Make dataset, Add dataset to datasets
        dataset = {}
        dataset['label'] = product_obj.product_name
        dataset['data'] = list(graph_inventory.values())
        datasets.append(dataset)

       
    # Get labels
    labels = []
    labels = graph_helpers.get_graph_labels(labels, start_date, end_date)


    context = {
        "labels": labels,
        "datasets": datasets
    }

    return render(request, 'catalog/graph.html', context)

def Schedule(request):
    # 스케줄 만드는 뷰

    if request.method == "POST":

        inventory_helpers.save_schedule(request.POST)
        return HttpResponseRedirect(reverse('index'))
        
        
    else:
        obj = list(Product.objects.all())
        context = {
        
            "product_list": obj
        }
        
    return render(request, "catalog/add_schedule.html", context)

def OrderFill(request, machine_num):
    # 오더에 생산량 분배량 넣는 뷰 

    if request.method == "POST":
        inventory_helpers.order_fill(request.POST)
        return HttpResponseRedirect(reverse('index'))

    else:

        orders = list(Order.objects.all().filter(machine_num=machine_num, order_date=date.today()))
        context = {
            "order_list": orders,
            "machine_num": machine_num,
        }

    return render(request, "catalog/order_fill.html", context)

# 재고 뷰들
class ResinListView(generic.ListView):
    model = Resin

class ProductListView(generic.ListView):
    model = Product

class ClientListView(generic.ListView):
    model = Client
