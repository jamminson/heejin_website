import re

with open('heejin/catalog/resin.csv', 'rb') as file:
    file = file.read()
    file = file.decode(encoding="utf_8_sig")

        # with open(file) as file:

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
        
# print(line_list)

def client_list(line_list):
    client = set()

    for line in line_list:
        client.add(line[1])

    print(client)
    print(len(client))

for i in range(len(line_list)):
    for j in range(3):
        line_list[i][j] = re.sub(r"\s+", "", line_list[i][j])

