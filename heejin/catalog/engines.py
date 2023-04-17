import csv
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

        
        for _ in file[1:]:
            _ = _.split(",")
            new_product = Product()
            
            link_client = Client.objects.get(client_name = _[0])
            link_resin = Resin.objects.get(resin_name = _[5])

            new_product.client_name = link_client
            new_product.model = _[1]
            new_product.product_code = _[2]
            new_product.product_name = _[3]
            new_product.machine_tonnage = _[4]
            new_product.resin = link_resin
            new_product.cavity = _[6]
            new_product.ct = _[7]
            new_product.week_produce = _[8]
            new_product.night_produce = _[9]
            new_product.real_weight = _[10]
            new_product.weight = _[11]
            new_product.save()

    
    def resin_csv_to_input(wrapper_file):

        file = wrapper_file.read()
        file = file.decode(encoding="utf_8_sig")
        file = file.split("\r\n")

        for _ in file[1:]:
            _ = _.split(",")
            new_resin = Resin()
            new_resin.material_type = _[0]
            link_client = Client.objects.get(client_name = _[1])
            new_resin.client_name = link_client
            new_resin.resin_name = _[2]
            new_resin.save()
        
        


                


