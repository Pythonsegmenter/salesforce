import pandas as pd
import os

def create_field_dataframes(obj_info, sf):
    field_dataframes = dict()
    for index, obj_label in enumerate(obj_info.loc[:, 'Label']):
        obj_api_name = obj_info.loc[index, "QualifiedApiName"]
        field_dataframes[obj_label] = pd.DataFrame(convert_query(sf.query(
            "SELECT QualifiedApiName, Label, DataType, Description, IsNillable, (SELECT IsLayoutable FROM Particles) FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName IN ('" + obj_api_name + "')")))
    return field_dataframes

def create_field_dataframes_api_names(obj_info, sf):
    """Same as other function but keys for dict are api names"""
    field_dataframes = dict()
    for obj_api_name in obj_info.loc[:, 'QualifiedApiName']:
        field_dataframes[obj_api_name] = pd.DataFrame(convert_query(sf.query(
            "SELECT QualifiedApiName, Label, DataType, Description, IsNillable, (SELECT IsLayoutable FROM Particles) FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName IN ('" + obj_api_name + "')")))
    return field_dataframes


def convert_query(query):
    """Converts the query to remove the weird dict from isLayoutable to a boolean"""
    for rec in query['records']:
        if (rec['Particles'] is not None):
            rec['IsLayoutable'] =rec['Particles']['records'][0]['IsLayoutable']
        else:
            rec['IsLayoutable']=False
        rec.pop('Particles', None) #Remove the particles part.
    return query['records']

def drop_attributes_column(dataframe):
    """drops a useless columns with attribute data that comes by default."""
    try:
        dataframe.drop('attributes', inplace=True, axis=1)  # This column is useless
    except:
        pass
    return dataframe

def create_SQL_query_string_from_list(item_list, parentheses_and_quotation_marks = True):
    if parentheses_and_quotation_marks:
        result_string = "("
        for item in item_list:
            result_string += "'" + item + "', "
        result_string = result_string[0:-2]
        result_string += ")"
    else:
        result_string = ""
        for item in item_list:
            result_string += item + ", "
        result_string = result_string[0:-2]
    return result_string

def convert_csv_files_to_dataframes_dict(csv_files_path):
    #Get the original descriptions
    csv_files = os.listdir(csv_files_path)
    dataframes = dict()
    for file in csv_files:
        dataframes[file] = pd.read_csv(csv_files_path + '/'+file)
    return dataframes