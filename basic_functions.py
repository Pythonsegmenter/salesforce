import pandas as pd


def create_field_dataframes(obj_api_name_and_label,sf):
    field_dataframes = dict()
    for obj_label in obj_api_name_and_label.loc[:,'Label']:
        field_dataframes[obj_label] = pd.DataFrame(sf.query(
        "SELECT QualifiedApiName, Label, DataType, Description FROM FieldDefinition WHERE EntityDefinition.Label IN ('"+ obj_label +"')")[
                                'records'])
    return field_dataframes

def create_SQL_query_string_from_list(item_list):
    result_string = "("
    for item in item_list:
        result_string += "'"+item+"', "
    result_string = result_string[0:-2]
    result_string+=")"
    return result_string