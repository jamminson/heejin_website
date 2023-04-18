import csv
import re
from .models import Client, Product, Resin

 
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

            
  



                


