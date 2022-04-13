import pandas as pd


def create_field_dataframes(obj_info, sf):
    field_dataframes = dict()
    for index, obj_label in enumerate(obj_info.loc[:, 'Label']):
        obj_api_name = obj_info.loc[index, "QualifiedApiName"]
        field_dataframes[obj_label] = pd.DataFrame(convert_query(sf.query(
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


def create_SQL_query_string_from_list(item_list):
    result_string = "("
    for item in item_list:
        result_string += "'" + item + "', "
    result_string = result_string[0:-2]
    result_string += ")"
    return result_string
