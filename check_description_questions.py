import basic_functions as bf
import pandas as pd


dataframes = bf.convert_files_to_dataframes_dict('questioned_descriptions')

#Compare each file and add a column with if the description changed or not
for file in dataframes.keys():
    list_with_questioned_descriptions = []
    dataframe = dataframes[file]

    for row, api_name in enumerate(dataframe.loc[:, "QualifiedApiName"]):


        #Compare the values
        if type(dataframe.loc[row,"Description"])==str:
            if dataframe.loc[row,"Description"][0]=="?":
                if "DataType" not in dataframe.columns:  # Catching empty dataframes
                    list_with_questioned_descriptions.append(
                        [dataframe.loc[row, "Label"], api_name, None,
                         dataframe.loc[row, "Description"]])
                else:
                    list_with_questioned_descriptions.append([dataframe.loc[row,"Label"], api_name,dataframe.loc[row,"DataType"], dataframe.loc[row,"Description"]])

    #save a new csv file with output if a description has changed.
    if len(list_with_questioned_descriptions)!=0:
        output_df = pd.DataFrame(list_with_questioned_descriptions, columns=['Label', 'QualifiedApiName', "DataType", 'questioned description'])
        output_df.to_csv('output/' + file, index=False)  # save the file

print("Done")