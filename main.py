import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType

def check_target_obj_links(data_type):
    """Returns link, link type, obj_label. Does this by checking the target object for look ups & master details"""
    if len(data_type)<6: #No look up or master detail, needed to check for index out of bounds
        return False, False, False
    elif data_type[0:7]=="Lookup(":
        return True, "Lookup", data_type[7:-1]
    elif data_type[0:14]=="Master-Detail(":
        return True, "Master-Detail", data_type[14:-1]
    #No look up or master detail but more then 6 characters
    return False, False, False

def check_link_non_target_obj(data_type, target_obj_label):
    """Returns link, link type, match with target object"""
    if len(data_type)<6: #No look up or master detail, needed to check for index out of bounds
        return False, False, False
    elif data_type[0:7]=="Lookup(":
        if data_type[7:-1]==target_obj_label:
            return True, "Lookup", True
        return True, "Lookup", False
    elif data_type[0:14]=="Master-Detail(":
        if data_type[14:-1]==target_obj_label:
            return True, "Master-Detail", True
        return True, "Master-Detail", False
    #No look up or master detail but more then 6 characters
    return False, False, False

## Connect with salesforce instance
loginInfo = json.load(open('login.json'))
username = loginInfo['username']
password = loginInfo['password']
security_token = loginInfo['security_token']
domain = 'login'
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id)

#Get datafram with all object api names that are customizable (=present in obj manager)
obj_api_name_and_label = pd.DataFrame(sf.query("SELECT QualifiedApiName, Label FROM EntityDefinition WHERE IsCustomizable=True")['records'])



#Set target label
target_label = "Account"

#Initialize link list & stat list
stat_list = [] #counts number of links
link_list = [] #details links

## Check in the target object to what other objects it references
#Get dataframe with field api names, labels & datatypes
field_info = pd.DataFrame(sf.query(
    "SELECT QualifiedApiName, Label, DataType, Description FROM FieldDefinition WHERE EntityDefinition.Label IN ('"+ target_label +"')")[
                            'records'])
for i,field_type in enumerate(field_info.loc[:,"DataType"]):
    link, link_type, obj_label = check_target_obj_links(field_type)
    if link:
        link_list.append([target_label, obj_label, link_type, field_info.loc[i,"Label"], field_info.loc[i,"Description"]])

## Check for other objects with references to the target object
#Iterate over the api names of all objects
for label in obj_api_name_and_label.loc[:, "Label"]: #Iterate over the api_names (string types)
    # print(label)
    if label == target_label: #We already checked the target object.
        continue

    #Get dataframe with field api names, labels & datatypes
    field_info = pd.DataFrame(sf.query(
        "SELECT QualifiedApiName, Label, DataType FROM FieldDefinition WHERE EntityDefinition.Label IN ('"+ label +"')")[
                                'records'])
    for i,field_type in enumerate(field_info.loc[:,"DataType"]):
        # print(field_type)
        link, link_type, target_obj_match = check_link_non_target_obj(field_type, target_label)
        if (link and target_obj_match):
            link_list.append([label, target_label, link_type, field_info.loc[i,"Label"], field_info.loc[i,"Description"]]) #Link list item: [source obj, target obj, link type, field name]

output = pd.DataFrame(link_list, columns=['Source obj', 'Target obj', "Link type", "Field name", "Field description"])
stat_list.append([target_label,output.shape[0]])
output.to_csv('/output/'+target_label+'.csv',index=False)
print("a")
        # print(field_info.loc[i,:])


#df_table.to_csv('entity definitions.csv',index=False)

#You have to say EntityDefintion.QualifiedApiName as if you would just say QualifiedApiName it would look at the FieldDefinition api name.
df_field = pd.DataFrame(sf.query("SELECT EntityDefinition.QualifiedApiName, QualifiedApiName, DataType FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName IN ('Account')")['records'])





print("a")
# df_field['TableName'] = df_field['EntityDefinition'].map(op.itemgetter('QualifiedApiName'))
# df_field[['TableName', 'QualifiedApiName', 'DataType']].head()

# metadata_org = sf.describe()
# # print(metadata_org['encoding'])
# # print(metadata_org['maxBatchSize'])
# # print(metadata_org['sobjects'])
# df_sobjects = pd.DataFrame(metadata_org['sobjects'])
# df_sobjects.to_csv('org metadata info.csv', index=False)


# method 1
# project__c = sf.Project__c
# metadata_project = project__c.metadata()
# df_project_metadata = pd.DataFrame(metadata_project.get('objectDescribe'))
# df_project_metadata.to_csv('project metadata.csv', index=False)


# method 2
# account = SFType('account', session_id, instance)
# account_metadata = account.metadata()
# df_account_metadata = pd.DataFrame(account_metadata.get('objectDescribe'))
# df_account_metadata.to_csv('account metadata.csv', index=False)