# Get all layer within .mxd project
# Use ArcGis Python console.
# Project mxd must be loaded n Arc Map

import arcpy
import os
import csv


# Define input .mxd directory location
PATH2 = r"C:\01_sig\mxd"

# Define input .mxd directory file
mxd_file = "inventaire.mxd"

# Define output directory
OUTPUT_PATH = r"C:\01_sig\output"

# Define output file name
output_file = os.path.join(OUTPUT_PATH, 'layers.csv')


arcpy.env.workspace = PATH2
arcpy.env.overwriteOutput = True
layers_list = []


for file in arcpy.ListFiles(mxd_file):
	mxd_path = os.path.join(PATH2,file)
	mxd = arcpy.mapping.MapDocument(mxd_path) 
	layers = arcpy.mapping.ListLayers(mxd)
	for layer in layers:
		if layer.supports("DATASOURCE"):
			fields = arcpy.ListFields(layer)
			layer_info = {
					"layer_name": layer.name.encode('utf-8'),
					"layer_source": layer.dataSource.encode('utf-8'),
					"layer_attributes": []}
			for field in fields:
				layer_info["layer_attributes"].append(
						(field.name.encode('utf-8'),field.type.encode('utf-8')))
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
					layer["layer_attributes"]])
		