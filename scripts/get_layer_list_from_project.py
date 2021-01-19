# Get all layer within .mxd project

import arcpy
import os
import csv


# Input .mxd directory location
PATH2 = r"C:\03_sig"

# Output file and directory
OUTPUT_PATH = r"C:\03_sig"
output_file = os.path.join(OUTPUT_PATH, 'layers.csv')


arcpy.env.workspace = PATH2
arcpy.env.overwriteOutput=True
layers_list = []


for file in arcpy.ListFiles("inventaire.mxd"):
	mxd_path = os.path.join(PATH2,file)
	mxd = arcpy.mapping.MapDocument(mxd_path) 
	layers = arcpy.mapping.ListLayers(mxd)
	for layer in layers:
		if layer.supports("DATASOURCE"):
			fields = arcpy.ListFields(layer)
			for field in fields:
				layer_info = {
					"layer_name": layer.name.encode('utf-8'),
					"layer_source": layer.dataSource.encode('utf-8'),
					"layer_field_name": field.name.encode('utf-8'),
					"layer_field_type": field.type.encode('utf-8')}
				layers_list.append(layer_info)



	with open(output_file, 'wb') as csvfile:
		filewriter = csv.writer(
				csvfile, delimiter=';',
				quotechar='"',
				quoting=csv.QUOTE_MINIMAL)
		for layer in layers_list:
			filewriter.writerow(
					[layer["layer_name"],
					layer["layer_source"],
					layer["layer_field_name"],
					layer["layer_field_type"]])
		