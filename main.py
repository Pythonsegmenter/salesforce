import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re

def check_string_match(searched_string, pattern):
    if pattern == searched_string: #Exact strings
        return True
    elif re.match(".*,"+pattern+".*",searched_string): #comma before
        return True
    elif re.match(".*"+pattern+",.*",searched_string): #comma after
        return True
    return False

def check_target_obj_links(data_type):
    """Returns link, link type, obj_label. Does this by checking the target object for look ups & master details"""
    if len(data_type)<6: #No look up or master detail, needed to check for index out of bounds
        return False, False, False
    elif data_type[0:7]=="Lookup(":
        if bc.relate_by_selection:
            in_selection_list = False
            for tar_label in bc.selection_list:
                if check_string_match(data_type[7:-1],tar_label):
                    in_selection_list=True
            if not in_selection_list:
                return False, False, False
        elif not bc.relate_by_selection:
            in_ignore_list=False
            for tar_label in bc.ignore_list:
                if check_string_match(data_type[7:-1],tar_label):
                    in_ignore_list=True
            if in_ignore_list:
                return False, False, False
        return True, "Lookup", data_type[7:-1]
    elif data_type[0:14]=="Master-Detail(":
        if bc.relate_by_selection:
            in_selection_list = False
            for tar_label in bc.selection_list:
                if check_string_match(data_type[14:-1],tar_label):
                    in_selection_list=True
            if not in_selection_list:
                return False, False, False
        elif not bc.relate_by_selection:
            in_ignore_list=False
            for tar_label in bc.ignore_list:
                if check_string_match(data_type[14:-1],tar_label):
                    in_ignore_list=True
            if in_ignore_list:
                return False, False, False
        return True, "Master-Detail", data_type[14:-1]
    #No look up or master detail but more then 6 characters
    return False, False, False

def check_link_non_target_obj(data_type, target_obj_label):
    """Returns link, link type, match with target object"""
    if len(data_type)<6: #No look up or master detail, needed to check for index out of bounds
        return False, False, False
    elif data_type[0:7]=="Lookup(":
        if check_string_match(data_type[7:-1],target_obj_label):
            return True, "Lookup", True
        return True, "Lookup", False
    elif data_type[0:14]=="Master-Detail(":
        if check_string_match(data_type[14:-1],target_obj_label):
            return True, "Master-Detail", True
        return True, "Master-Detail", False
    #No look up or master detail but more then 6 characters
    return False, False, False

## Connect with salesforce instance
loginInfo = json.load(open(bc.login))
username = loginInfo['username']
password = loginInfo['password']
security_token = loginInfo['security_token']
domain = bc.domain
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id)

#Get dataframewith all object api names that are customizable (=present in obj manager) and present in the selection list or not present in the ignore list.
api_ignore_string = bf.create_SQL_query_string_from_list(bc.api_ignore_list) #The list of objects with api names mentioned in here will always be ignored. (for objects with duplicate labels)
if bc.relate_by_selection:
    select_string = bf.create_SQL_query_string_from_list(
        bc.selection_list)  # create string of list of objects to ignore for SQL query
    obj_info = pd.DataFrame(sf.toolingexecute("query/?q=SELECT+"+bc.object_properties+"+from+EntityDefinition+Where+IsCustomizable=True+AND+Label+IN+"+select_string+"+AND+QualifiedApiName+NOT+IN+"+api_ignore_string)['records'])
    # obj_info = pd.DataFrame(sf.query("SELECT "+bc.object_properties+" FROM EntityDefinition WHERE IsCustomizable=True AND Label IN " + select_string)[
    #                                       'records'])
else:
    if len(bc.ignore_list)!=0: #Only do this if there is something to ignore
        ignore_string = bf.create_SQL_query_string_from_list(bc.ignore_list) #create string of list of objects to ignore for SQL query
        obj_info = pd.DataFrame(sf.toolingexecute(
            "query/?q=SELECT+" + bc.object_properties + "+from+EntityDefinition+Where+IsCustomizable=True+AND+Label+NOT+IN+" + ignore_string+"+AND+QualifiedApiName+NOT+IN+"+api_ignore_string)[
                                    'records'])
        # obj_info = pd.DataFrame(sf.query("SELECT " + bc.object_properties + " FROM EntityDefinition WHERE IsCustomizable=True AND Label NOT IN " + ignore_string)['records'])
    else:
        obj_info = pd.DataFrame(sf.toolingexecute(
            "query/?q=SELECT+" + bc.object_properties + "+from+EntityDefinition+Where+IsCustomizable=True+AND+QualifiedApiName+NOT+IN+"+api_ignore_string)[
                                    'records'])
field_dataframes_dict = bf.create_field_dataframes(obj_info, sf) #a dict with as keys the object labels and as values the dataframes of the objects' fields.

if bc.print_fields:
    for obj_label in field_dataframes_dict:
        field_dataframes_dict[obj_label].drop('attributes',inplace=True, axis=1) #This column is useless
        field_dataframes_dict[obj_label].to_csv('output/' + obj_label + '_fields.csv', index=False)  # save the file
    obj_info.drop('attributes', inplace=True, axis=1)  # This column is useless
    obj_info.to_csv('output/a_object_info_no_links.csv',index=False)

if bc.print_links:
    #Initialize stat list
    stat_list = [] #counts number of links per obj

    stop_index =0 #For testing

    ## Check for other objects with references to the target object
    #Iterate over the api names of all objects
    for index, target_label in enumerate(obj_info.loc[:, "Label"]): #Iterate over the api_names (string types)
        #get target API name
        target_api_name = obj_info.loc[index, "QualifiedApiName"]

        #For testing purposes
        if bc.stop_limit == stop_index:
            break
        stop_index += 1

        #Initialize link list
        link_list = [] #details links


        ## Check in the target object to what other objects it references
        #Get dataframe with field api names, labels & datatypes
        field_info = field_dataframes_dict[target_label]
        if "DataType" not in field_info.columns:  # Catching empty dataframes
            print("No data type for " + target_label)
            continue
        for i,field_type in enumerate(field_info.loc[:,"DataType"]):
            link, link_type, obj_label = check_target_obj_links(field_type)
            if link:
                link_list.append([target_label, obj_label, link_type, field_info.loc[i,"Label"], field_info.loc[i,"QualifiedApiName"], field_info.loc[i,"Description"],not field_info.loc[i,"IsNillable"]])

        links_to_other_objects = len(link_list)

        ## Check for other objects with references to the target object
        #Iterate over the api names of all objects
        for label in obj_info.loc[:, "Label"]: #Iterate over the api_names (string types)
            # print(label)
            if label == target_label: #We already checked the target object.
                continue

            #Get dataframe with field api names, labels & datatypes
            field_info = field_dataframes_dict[label]
            if "DataType" not in field_info.columns: #Catching empty dataframes
                print("No data type for "+label)
                continue
            for i,field_type in enumerate(field_info.loc[:,"DataType"]):
                # print(field_type)
                link, link_type, target_obj_match = check_link_non_target_obj(field_type, target_label)
                if (link and target_obj_match):
                    link_list.append([label, target_label, link_type, field_info.loc[i,"Label"], field_info.loc[i,"QualifiedApiName"], field_info.loc[i,"Description"], not field_info.loc[i,"IsNillable"]]) #Link list item: [source obj, target obj, link type, field name]

        output = pd.DataFrame(link_list, columns=['Source obj', 'Target obj', "Link type", "Field name", "Field API name", "Field description", "Is Required"])
        links_from_other_objects = len(link_list) - links_to_other_objects
        try:
            record_count = sf.query("SELECT COUNT() FROM "+target_api_name)['totalSize']
        except:
            print("Couldn't get count from "+target_api_name)
            record_count = None
        stat_list.append([output.shape[0], links_to_other_objects, links_from_other_objects, record_count]) #add the statistics

        #Avoid annoying / character in the "Account / BU" object.
        if target_label.find("/")!=-1:
            annoying_index = target_label.find("/")
            target_label = target_label[0:annoying_index]+" per "+target_label[annoying_index+1:]

        output.to_csv('output/'+target_label+'.csv',index=False) #save the file

    stats = pd.DataFrame(stat_list, columns=['number of links', 'number of outgoing links', 'number of incoming links','number of records'])
    obj_info.drop('attributes',inplace=True,axis=1) #This column is useless
    concat = pd.concat([obj_info, stats], axis=1) #merge the object relation info with regular object info
    concat.to_csv('output/a_object_info.csv',index=False)
print("Done")
