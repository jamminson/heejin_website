from datetime import date, timedelta



class graph_helpers():

    def date_product_string_encoder(start_date, end_date, product_list):

        # Need to pass the start and end dates + products into the graph view. 
        # Combine the dates by + and products by +
        # 'date_string@&@product_string'

        product_string = "+".join(product_list)
        date_string = start_date + "+" + end_date
        return date_string + "@&@" + product_string
    
    def date_product_string_decoder(date_product_string):
        [date_string, product_string] = date_product_string.split("@&@")

        # [product1, product2, ...]
        product_l = product_string.split("+")

        # start_date & end_dates ISOFORMAT -> Datetime.date format 하기
        # https://docs.python.org/3/library/datetime.html#date-objects
        [start_date, end_date] = date_string.split("+")
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        return start_date, end_date, product_l
    
    def inventory_dict2graph_inventory_dict(inventory, graph_inventory, graph_start_date, graph_end_date, first_order_date):
        graph_total_days = graph_end_date - graph_start_date
        for x in range(graph_total_days+1):

                if first_order_date <= (graph_start_date + timedelta(days=x)) <= date.today():
                    graph_inventory[(graph_start_date + timedelta(days=x)).isoformat()] = inventory[(graph_start_date + timedelta(days=x))]
                
                elif (graph_start_date + timedelta(days=x)) < first_order_date:
                    graph_inventory[(graph_start_date + timedelta(days=x)).isoformat()] = 0
                
                elif (graph_start_date + timedelta(days=x)) > date.today():
                    graph_inventory[(graph_start_date + timedelta(days=x)).isoformat()] = inventory[date.today()]
        
        return graph_inventory
    
    def empty_inventory_dict2graph_inventory_dict(graph_inventory, graph_start_date, graph_end_date):
        graph_total_days = (graph_end_date - graph_start_date).days
        for x in range(graph_total_days+1):
            graph_inventory[(graph_start_date + timedelta(days=x)).isoformat()] = 0
        
        return graph_inventory
    
    def get_graph_labels(labels, start_date, end_date):
        total_days = (end_date - start_date).days
        for x in range(total_days+1):
            labels.append(start_date + timedelta(days=x))
        
        return labels


        
    

