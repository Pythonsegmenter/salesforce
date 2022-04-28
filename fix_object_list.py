import pandas as pd
import basic_functions as bf
import re

dataframe_dict = bf.convert_files_to_dataframes_dict("input")
dataframe = dataframe_dict['object categorisation.xlsx']

#Go over all incorrect object names and see if they are present in the correct object names. Print any objects that are not present.
data_list = []
for api_name in dataframe.loc[:,"QualifiedApiName"]:
    label = bf.find_value_based_on_column_name_and_other_value(dataframe,"QualifiedApiName",api_name,"Label")
    description = bf.find_value_based_on_column_name_and_other_value(dataframe,"QualifiedApiName",api_name,"Description")
    records = bf.find_value_based_on_column_name_and_other_value(dataframe,"QualifiedApiName",api_name,"number of records")
    found = dataframe.index[dataframe["API name"] == api_name].tolist()
    if len(found)==1:
        index = found[0]
        salesforce_product = dataframe["Salesforce product"].iloc[index]
        subsection = dataframe["Subsection"].iloc[index]
        explain = dataframe["to be explained in documentation?"].iloc[index]
        usage = dataframe["Object usage"].iloc[index]
        if type(description)==float:
            description = dataframe["Object description & important remarks"].iloc[index]
        covered = dataframe["Covered by documentation"].iloc[index]
    else:
        salesforce_product = None
        subsection = None
        explain = None
        usage = None
        covered = None
    data_list.append([label,api_name,records,description,salesforce_product,subsection,explain,usage,covered])
data = pd.DataFrame(data_list, columns=['Label', 'QualifiedApiName', 'Records','Description','Salesforce product', 'Subsection', 'To be explained in documentation?',"Object usage","Covered by documentation"])
data.to_excel('output/object categorisation.xlsx')


    # if type(api_name)!=float:
    #     found = dataframe.index[dataframe["API name"] == api_name].tolist()
    #     if len(found)!=1:
    #         print(api_name, len(found))

#Go over all correct object names, if they are in the incorrect object names then take all data and add a row. If they are not present just add a row. Save .xlsx
print("a")