import pandas as pd
import os
import numpy as np

#Get the original descriptions
original_csv_files = os.listdir('original_descriptions')
original_dataframes = dict()
for file in original_csv_files:
    original_dataframes[file] = pd.read_csv('original_descriptions/'+file)

#Get the new descriptions
new_csv_files = os.listdir('new_descriptions')
new_dataframes = dict()
for file in new_csv_files:
    new_dataframes[file] = pd.read_csv('new_descriptions/'+file)

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
        print(new_description_row["Description"].iloc[0])
        print(type(new_description_row["Description"].iloc[0]))
        if (old_description_row["Description"].iloc[0]!=new_description_row["Description"].iloc[0]) and (type(old_description_row["Description"].iloc[0])==str or type(new_description_row["Description"].iloc[0])==str): #string type check needed because stupid nan types are never equal. So at least one of the two must also be a string.
            list_with_changed_descriptions.append([old_description_row["Label"].iloc[0],api_name,old_description_row["Description"].iloc[0],new_description_row["Description"].iloc[0]])

    #save a new csv file with output if a description has changed.
    if len(list_with_changed_descriptions)!=0:
        output_df = pd.DataFrame(list_with_changed_descriptions, columns=['Label','QualifiedApiName', 'original description', 'new description'])
        output_df.to_csv('output/' + file, index=False)  # save the file



print("a")

#df = pd.read_csv('data.csv')