import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re

def get_field_record_count(field_api_names, list_of_field_labels, obj_api_name, print_field_record_data = False):
    select_field_string = bf.create_SQL_query_string_from_list(field_api_names,parentheses_and_quotation_marks=False)
    field_record_data = pd.DataFrame(sf.query("SELECT "+select_field_string+" FROM Account")['records'])
    # field_record_data = pd.DataFrame(sf.query("SELECT AccountNumber FROM Account")['records'])
    field_record_data = bf.drop_attributes_column(field_record_data) #drops a useless columns with attribute data that comes by default.
    #Print the field record data if requested.
    if print_field_record_data:
        field_record_data.to_csv('output/'+obj_api_name+'_field_record_data.csv',index=False)

    field_record_count_list = []
    for i, field in enumerate(field_record_data.columns): #iterate over fields
        record_counter = 0
        for record in field_record_data.loc[:,field]: #iterate over records in fields
            if record!=None:
                record_counter+=1
        field_record_count_list.append([list_of_field_labels[i],field,record_counter,len(field_record_data.loc[:field])])
    field_record_count_df = pd.DataFrame(field_record_count_list,columns=['Field label', 'Field Api Name','Records with field filled in', 'Total records'])

    return field_record_count_df

## Connect with salesforce instance
loginInfo = json.load(open(bc.login))
username = loginInfo['username']
password = loginInfo['password']
security_token = loginInfo['security_token']
domain = bc.domain
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id)

#Choose the objects you want to get info about (bc.selection_list_api_names)
select_string = bf.create_SQL_query_string_from_list(bc.selection_list_api_names)  # create string of list of objects to ignore for SQL query
obj_info = pd.DataFrame(sf.toolingexecute(
    "query/?q=SELECT+" + bc.object_properties + "+from+EntityDefinition+Where+IsCustomizable=True+AND+QualifiedApiName+IN+" + select_string)[
                            'records'])
#Get dataframes with field information for each of those objects.
field_data_frames = bf.create_field_dataframes_api_names(obj_info,sf)


for obj_api_name in field_data_frames.keys():
    field_data_frame = field_data_frames[obj_api_name]
    list_of_field_api_names = list(field_data_frame.loc[:, "QualifiedApiName"])
    list_of_field_labels = list(field_data_frame.loc[:, "Label"])
    field_record_count = get_field_record_count(list_of_field_api_names, list_of_field_labels, obj_api_name, print_field_record_data=bc.print_records)

    #print the result
    field_record_count.to_csv('output/'+obj_api_name+'_field_record_count.csv',index=False)


print('Done')