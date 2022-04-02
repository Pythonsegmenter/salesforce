import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType

def check_link(data_type, target_obj_label):
    """Returns link, link type, match with target object"""
    if len(data_type)<6: #No look up or master detail
        return False, False, False
    elif data_type[0:7]=="Lookup(":
        if data_type[7:-1]==target_obj_label:
            return True, "Lookup", True
        return True, "Lookup", False
    elif data_type[0:14]=="Master-Detail(":
        if data_type[14:-1]==target_obj_label:
            return True, "Master-Detail", True
        return True, "Master-Detail", False

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

target_label = "Account"

#Iterate over the api names of all objects
for label in obj_api_name_and_label.loc[:, "Label"]: #Iterate over the api_names (string types)
    print(label)

    #Get dataframe with field api names, labels & datatypes
    field_info = pd.DataFrame(sf.query(
        "SELECT QualifiedApiName, Label, DataType FROM FieldDefinition WHERE EntityDefinition.Label IN ('"+ label +"')")[
                                'records'])
    for i,field_type in enumerate(field_info.loc[:,"DataType"]):
        print(field_type)
        link, link_type, target_obj_match = check_link(field_type,target_label)
        if (link and target_obj_match):
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