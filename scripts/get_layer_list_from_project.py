# Get all layer within .mxd project
# Use ArcGis Python console.
# Project mxd must be loaded n Arc Map

import arcpy
import os
import csv


# Select input .mxd directory location
mxd_directory = r"\\astrolab\MXD"

# Select input .mxd directory file
mxd_file = "SuresnesIntranet.mxd"

# Select output directory
output_directory = r"C:\01_sig\projets\202101_inventaire\output"

# Define output file name
output_file_name = "suresnesintranet_layers.csv"


output_file = os.path.join(output_directory, output_file_name)
error_output_file = os.path.join(output_directory,  "error_" + output_file_name)
arcpy.env.workspace = mxd_directory
arcpy.env.overwriteOutput = True
layers_list = []
layers_rejected_list = []

for file in arcpy.ListFiles(mxd_file):
	mxd_path = os.path.join(mxd_directory,file)
	mxd = arcpy.mapping.MapDocument(mxd_path) 
	layers = arcpy.mapping.ListLayers(mxd)
	for layer in layers:
		if layer.supports("DATASOURCE"):
			try:
				fields = arcpy.ListFields(layer)
				txt = layer.dataSource

				layer_source = txt.replace('C:\\Users\\adminabaaboua\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\aop@sig.sde\\', '')
				print (layer_source)

				layer_info = {
						"layer_name": layer.name.encode('utf-8'),
						"layer_source": layer_source.encode('utf-8'),
						"layer_attributes": []}

				for field in fields:
					layer_info["layer_attributes"].append(
							(field.name.encode('utf-8'),field.type.encode('utf-8')))
				layers_list.append(layer_info)

			except:
				layers_rejected_list.append(layer.name.encode('utf-8'))
				pass

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

	with open(error_output_file, 'wb') as csvfile:
		filewriter = csv.writer(
				csvfile, delimiter=';',
				quotechar='"',
				quoting=csv.QUOTE_MINIMAL)
		for layer in layers_rejected_list:
			filewriter.writerow(
					[layer])
		