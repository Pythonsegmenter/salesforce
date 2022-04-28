import pandas as pd
import os
import basic_functions as bf
import numpy as np



original_dataframes = bf.convert_files_to_dataframes_dict('original_descriptions')
new_dataframes = bf.convert_files_to_dataframes_dict('new_descriptions')

#Compare each file and add a column with if the description changed or not
for file in original_dataframes.keys():
    list_with_changed_descriptions = []
    original_dataframe = original_dataframes[file]
    try:
        new_dataframe = new_dataframes[file]
    except KeyError:
        raise KeyError(file + " not found in new objects")

    for api_name in original_dataframe.loc[:,"QualifiedApiName"]:
        #Get the row with te current api name
        old_description_row = original_dataframe.loc[original_dataframe['QualifiedApiName'] == api_name]
        new_description_row= new_dataframe.loc[new_dataframe['QualifiedApiName'] == api_name]

        #Check that a row is found
        if len(new_description_row)!=1:
            print(api_name + " of file "+file+" is not found in the new descriptions.")
            continue

        #Compare the values
        if (old_description_row["Description"].iloc[0]!=new_description_row["Description"].iloc[0]) and (type(old_description_row["Description"].iloc[0])==str or type(new_description_row["Description"].iloc[0])==str): #string type check needed because stupid nan types are never equal. So at least one of the two must also be a string.
            list_with_changed_descriptions.append([old_description_row["Label"].iloc[0],api_name,old_description_row["Description"].iloc[0],new_description_row["Description"].iloc[0]])

    #save a new csv file with output if a description has changed.
    if len(list_with_changed_descriptions)!=0:
        output_df = pd.DataFrame(list_with_changed_descriptions, columns=['Label','QualifiedApiName', 'original description', 'new description'])
        output_df.to_csv('output/' + file, index=False)  # save the file



print("Done")

#df = pd.read_csv('data.csv')