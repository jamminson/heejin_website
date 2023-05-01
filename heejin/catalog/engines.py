import csv
import re
from .models import Client, Product, Resin, Order
from datetime import date, timedelta

 
class engines():

    def __init__(self) -> None:
        pass

    def client_csv_to_input(wrapper_file):

        file = wrapper_file.read()
        file = file.decode(encoding="utf_8_sig")
        file = file.split("\r\n")

        for _ in file[1:]:
            new_client = Client()
            new_client.client_name = _
            new_client.save()


    def product_csv_to_input(wrapper_file):

        file = wrapper_file.read()
        file = file.decode(encoding="utf_8_sig")
        file = file.split("\r\n")
        # At this point, the file is a list of elements of whole entries as one string. 

        # print(file)

        line_list = []
        for line in file[1:]:
            line_list.append(line.split(","))
        
        for i in range(len(line_list)):
            for j in range(len(line_list[i])):
                
                line_list[i][j] = re.sub(r"/", "", line_list[i][j])
                line_list[i][j] = re.sub(r"\s+", "", line_list[i][j])
                
            
            line_list[i].pop(0)
        
    
            
            (link_client, client_created_bool) = Client.objects.get_or_create(client_name = line_list[i][0])
            (link_resin,  resin_created_bool) = Resin.objects.get_or_create(resin_name = line_list[i][5])

            obj_product = Product(client_name=link_client, 
                                  model=line_list[i][1],
                                  product_code=line_list[i][2],
                                  product_name=line_list[i][3],
                                  machine_tonnage=line_list[i][4],
                                  resin=link_resin,
                                  cavity=line_list[i][6],
                                  ct=line_list[i][7],
                                  week_produce=line_list[i][8],
                                  night_produce=line_list[i][9],
                                  real_weight=line_list[i][10],
                                  weight=line_list[i][11])
            
            obj_product.save()

            # new_product.client_name = link_client
            # new_product.model = _[1]
            # new_product.product_code = _[2]
            # new_product.product_name = _[3]
            # new_product.machine_tonnage = _[4]
            # new_product.resin = link_resin
            # new_product.cavity = _[6]
            # new_product.ct = _[7]
            # new_product.week_produce = _[8]
            # new_product.night_produce = _[9]
            # new_product.real_weight = _[10]
            # new_product.weight = _[11]
            # new_product.save()

    
    def resin_csv_to_input(wrapper_file):

        file = wrapper_file.read()
        file = file.decode(encoding="utf_8_sig")


        file = file.split("\n")

        line_list = []

        for line in file[1:]:
            line_list.append(line.split(","))
            
        for i in range(len(line_list)):
            for j in range(len(line_list[i])):
                line_list[i][j] = line_list[i][j].strip()
        
        for i in range(len(line_list)):

            if len(line_list[i]) != 3:
                line_list.pop(i)
                continue
            
            if line_list[i][1] == "":
                line_list[i][1] = "empty"

        for i in range(len(line_list)):
            for j in range(3):
                line_list[i][j] = re.sub(r"\s+", "", line_list[i][j])

        for i in range(1, len(line_list)):
            print(line_list[i][1])
            new_resin = Resin(material_type = line_list[i][0], client_name = Client.objects.get(client_name = line_list[i][1]), resin_name=line_list[i][2])
            new_resin.save()

    def clean_order_list(order_list):
        volume_change = []
        for order in order_list:
            changed = False
            vol = order_list[0].produced - order_list[0].distributed

            for i in range(len(volume_change)):
                if order.order_date == volume_change[i][0]:
                    volume_change[i][1] += vol
                    changed = True
            
            if not changed:
                volume_change.append((order.order_date, vol))
                
        
        print(volume_change)
            


            
           



    def order2inventory_dictionary(order_qlist, start_date, end_date):

        #Should output: iterator of dates, iterator of volumes. 

        # Order_list is an iterator of order classes. Orders are ordered from earliest date.
        # Program outputs dictionary of which keys are ISOFORMAT dates and values are the corresponding inventory sizes.
        if len(order_qlist) != 0:

            order_list = list(order_qlist)
            volume_change = []
            for order in order_list:
                vol = order.produced - order.distributed
                changed = False

                for i in range(len(volume_change)):
                    if order.order_date == volume_change[i][0]:
                        volume_change[i][1] += vol
                        changed = True
                
                if not changed:
                    volume_change.append([order.order_date, vol])

        

            inventory = {}
            first_date = order_list[0].order_date
            total_days = (date.today() - first_date).days
            

            for x in range(total_days+1):
                inventory[(first_date + timedelta(days=x))] = 0
            inventory[first_date] = order_list[0].produced - order_list[0].distributed
            volume_change.pop(0)


            inventory_date_list = list(inventory.keys())
            for i in range(1, len(inventory_date_list)):

                if len(volume_change) == 0:
                    inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]]
                
                else:
                    
                    if inventory_date_list[i] == volume_change[0][0]:
                        print("hi")
                        inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]] + volume_change[0][1]
                        volume_change.pop(0)
                    
                    else:
                        inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]]
            
            print(inventory)


            graph_inventory = {}
            graph_total_days = (end_date - start_date).days
            for x in range(graph_total_days+1):

                if first_date<= (start_date + timedelta(days=x)) <= date.today():
                    graph_inventory[(start_date + timedelta(days=x)).isoformat()] = inventory[(start_date + timedelta(days=x))]
                
                elif (start_date + timedelta(days=x)) < first_date:
                    graph_inventory[(start_date + timedelta(days=x)).isoformat()] = 0
                
                elif (start_date + timedelta(days=x)) > date.today():
                    graph_inventory[(start_date + timedelta(days=x)).isoformat()] = inventory[date.today()]


            
            
        
        else:
            graph_inventory = {}
            graph_total_days = (end_date - start_date).days
            for x in range(graph_total_days+1):
                graph_inventory[(start_date + timedelta(days=x)).isoformat()] = 0
        
        return graph_inventory.values()
            
            



    def schedule_order_input(request_post_dict):

        for k, v in request_post_dict.items():
            
        
            if v == 'on':
                new_order = Order(order_date=date.fromisoformat(request_post_dict["order_date"]),
                                  machine_num=int(request_post_dict['machine_num']),
                                  product=Product.objects.get(product_name=k),
                                  )
                new_order.save()
        
    def order_fill(request_post_dict):

        for k, v in request_post_dict.items():
            
            if k == "csrfmiddlewaretoken":
                continue

            order = Order.objects.get(product=Product.objects.get(product_name=k))
            order.produced = int(v)
            order.save()



    def get_today_date():
        return date.today()


