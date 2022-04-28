import pandas as pd
import basic_functions as bf

dataframes_dict = bf.convert_files_to_dataframes_dict('input')

for file in dataframes_dict.keys():
    dataframe = dataframes_dict[file]
    api_names = list()
    labels = list()
    for api_name in dataframe.loc[:,"QualifiedApiName"]:
        api_names.append(api_name)
    for label in dataframe.loc[:,"Label"]:
        labels.append(label)
    print("API: "+str(api_names))
    print("Label: "+str(labels))