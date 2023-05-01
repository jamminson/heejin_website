from .models import Product, Order
from datetime import date, timedelta


class inventory_helpers():

    def __init__(self) -> None:
        pass

    def order_qlist2order_volume(order_qlist):
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
        
        return volume_change  

    def volume_list2inventory_dict(volume_change, inventory):

        inventory_date_list = list(inventory.keys())
        for i in range(1, len(inventory_date_list)):

            if len(volume_change) == 0:
                inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]]
            
            else:
                
                if inventory_date_list[i] == volume_change[0][0]:
                    inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]] + volume_change[0][1]
                    volume_change.pop(0)
                
                else:
                    inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]]
        
        return inventory



    # def order2inventory_dictionary(order_volume_change, start_date, end_date):

    #     #Should output: iterator of dates, iterator of volumes. 

    #     # Order_list is an iterator of order classes. Orders are ordered from earliest date.
    #     # Program outputs dictionary of which keys are ISOFORMAT dates and values are the corresponding inventory sizes.
    #     if len(order_volume_change) != 0:


    #         inventory = {}
    #         first_date = order_volume_change[0][0]
    #         total_days = (date.today() - first_date).days
            

    #         for x in range(total_days+1):
    #             inventory[(first_date + timedelta(days=x))] = 0
    #         inventory[first_date] = order_volume_change[0][1]
    #         order_volume_change.pop(0)


    #         inventory_date_list = list(inventory.keys())
    #         for i in range(1, len(inventory_date_list)):

    #             if len(order_volume_change) == 0:
    #                 inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]]
                
    #             else:
                    
    #                 if inventory_date_list[i] == order_volume_change[0][0]:
    #                     inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]] + order_volume_change[0][1]
    #                     order_volume_change.pop(0)
                    
    #                 else:
    #                     inventory[inventory_date_list[i]] = inventory[inventory_date_list[i-1]]
            
    #         return inventory
            
            
            
    
            
    #     else:
    #         graph_inventory = {}
    #         graph_total_days = (end_date - start_date).days
    #         for x in range(graph_total_days+1):
    #             graph_inventory[(start_date + timedelta(days=x)).isoformat()] = 0
        
    #     return graph_inventory.values()
            
            

    def setup_inventory_dict(inventory, first_order):
        total_days = (date.today() - first_order[0]).days
            
        for x in range(total_days+1):
            inventory[(first_order[0] + timedelta(days=x))] = 0
        inventory[first_order[0]] = first_order[1]

        return inventory

    def save_schedule(request_post_dict):
        # 스케줄를 Order model로 입력하기

        for k, v in request_post_dict.items():
            
        
            if v == 'on':
                new_order = Order(order_date=date.fromisoformat(request_post_dict["order_date"]),
                                  machine_num=int(request_post_dict['machine_num']),
                                  product=Product.objects.get(product_name=k),
                                  )
                new_order.save()
        
    def order_fill(request_post_dict):
        # Order model내 생산량 분배량 입력

        for k, v in request_post_dict.items():
            
            if k == "csrfmiddlewaretoken":
                continue

            order = Order.objects.get(product=Product.objects.get(product_name=k))
            order.produced = int(v)
            order.save()



