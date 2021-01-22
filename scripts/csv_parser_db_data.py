import csv
import os
from re import sub, split

# Select input directory
input_directory = r"C:\01_sig\projets\202101_vieassociative"

# Select input .csv  file name
input_file_name = "address_only_db.csv"

# Select output directory
output_directory = r"C:\01_sig\projets\202101_vieassociative\output"

# Define output .csv file name
output_file_name = "output_db_address.csv"

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
        long_add = row[4].lower()
        
        while "  " in long_add:
            long_add = long_add.replace("  ", " ")

   
        hnr, street_name = create_street_name(long_add)
        address = hnr + ' ' + street_name 
        address = address.strip(' ')

        object_id= row[0]
        x = row[1]
        y = row[2]
        postal_code = row[3]
        address = long_add

        db_address = {
            'object_id' : object_id,
            'lon' : x,
            'lat' : y,
            'postal_code' : postal_code,
            'address' : address
        }
        address_list.append(db_address)

with open(output_file, 'w', newline='') as csvfile:
    filewriter = csv.writer(
            csvfile, delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
    for addr in address_list:
        filewriter.writerow(
                [addr["object_id"],
                addr["lon"],
                addr["lat"],
                addr["postal_code"],
                addr["address"]])

