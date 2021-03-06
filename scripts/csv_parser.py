import csv
import os
from re import sub, split
import unicodedata

# Select input directory
input_directory = r"C:\01_sig\projets\202101_vieassociative"

# Select input .csv  file name
input_file_name = "address_only.csv"

# Select output directory
output_directory = r"C:\01_sig\projets\202101_vieassociative\output"

# Define output .csv file name
output_file_name = "output_association2.csv"

input_file = os.path.join(input_directory, input_file_name)
output_file = os.path.join(output_directory, output_file_name)

address_list = []

def create_street_name(elements):
    street_name = ''
    hnr = ''
    counter = 0
    for element in elements:
        if counter == 0:
            hnr = element
        else:
            street_name += element + ' '
        counter += 1
    return hnr, street_name


with open(input_file, 'r') as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        long_add = row[0].lower()
        long_add = sub(',','',long_add)
        long_add = unicodedata.normalize(u'NFKD', long_add).encode('ascii', 'ignore').decode('utf8')

        
        while "  " in long_add:
            long_add = long_add.replace("  ", " ")

        long_add = split(" ", long_add)
        
        hnr, street_name = create_street_name(long_add)
        address = hnr + ' ' + street_name 
        address = address.strip(' ')

        # id_association = row[1].encode('utf-8')
        # address = address.encode('utf-8')
        # postal_code = row[2].encode('utf-8')

        id_association = row[1]
        address = address
        postal_code = row[2]

        id_association = id_association.lower()
        address = address.lower()
        postal_code = postal_code.lower()

        association = {
            'id_association' : id_association,
            'address' : address,
            'postal_code' : postal_code
        }
        address_list.append(association)

with open(output_file, 'w', newline='') as csvfile:
    filewriter = csv.writer(
            csvfile, delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
    for layer in address_list:
        filewriter.writerow(
                [layer["id_association"],
                layer["address"],
                layer["postal_code"]])

