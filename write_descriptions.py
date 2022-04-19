import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re


## Connect with salesforce instance
loginInfo = json.load(open(bc.login))
username = loginInfo['username']
password = loginInfo['password']
security_token = loginInfo['security_token']
domain = bc.domain
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id)

mdapi = sf.mdapi

dataframe_dict = bf.convert_csv_files_to_dataframes_dict('write_descriptions')
for dataframe_key in dataframe_dict:
    if bf.query_yes_no("Are you sure you want to re-write descriptions for " + dataframe_key + "?"):
        #read the descriptions of all fields
        dataframe = dataframe_dict[dataframe_key]
        object_api_name = dataframe_key[0:dataframe_key.find("_field")]
        custom_object = mdapi.CustomObject.read("object_api_name")
        #find see if there are changes


        #write the changes
        for i, field_api_name in enumerate(dataframe.loc[:, "QualifiedApiName"]):
            description = dataframe.loc[i,"Description"]

            custom_field = mdapi.CustomField(
                fullName = "AccountNumber",
                description = "Not used",
                inlineHelpText = "Not used"
            )
        custom_object.fields = [custom_field]

        mdapi.CustomObject.update(custom_object)
        print("Done")