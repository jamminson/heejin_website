from datetime import date, timedelta

class ord():

    ord_date = date
    vol = int

start_date = date(2023, 3, 1)
end_date = date(2023, 3, 5)


# User inputs start date, end date, product.
# Output pairs of a day and the amount of the product at that point.
# Orders are an iterator of order classes. Orders are ordered from earliest date.
# Program outputs dictionary of which keys are ISOFORMAT dates and values are the corresponding inventory sizes.

"""
1. Produce a list w len = no. days. (Assumes timescale is days that we want). Each element is a dictionary.  
2. Calculate inventory list.
3. Iterate through each date in the list. If the date matches then do relavent calculation based on previous date.
4. Computer inventory list.

""" 

init_value = 100
inventory = {}
num_days = (end_date - start_date).days

for x in range(num_days+1):
    inventory[(start_date + timedelta(days=x))] = 0

inventory[start_date] = init_value


query_list = []

class ord():

    ord_date = date
    vol = int

a = ord()
a.ord_date = date(2023, 3, 2)
a.vol = 100

b = ord()
b.ord_date = date(2023, 3, 1)
b.vol = 100

query_list.append(b)
query_list.append(a)

for elm in inventory:

    if len(query_list) > 0:

        if elm == query_list[0].ord_date:
            print("here1")
            if elm != start_date:
                inventory[elm] = inventory[elm - timedelta(days=1)] + query_list[0].vol
                query_list.pop(0)
            
            else:
                inventory[elm] = inventory[elm] + query_list[0].vol
                query_list.pop(0)
        
        else:
            print("here2")
            if elm != start_date:
                inventory[elm] = inventory[elm - timedelta(days=1)]
            
            else:
                continue
    
    else:
        if elm != start_date:
                    inventory[elm] = inventory[elm - timedelta(days=1)]
        else:
            continue
            




print(inventory)
print(query_list)

prep_inventory = {}
for i in inventory:
     prep_inventory[i.isoformat()] = inventory[i]

print(prep_inventory)