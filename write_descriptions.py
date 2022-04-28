import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re

def convert_empty_to_none(input):
    """Without this function empty fields will be written as None or nan-strings"""
    if type(input)!=str:
        input = str(input)
    if (input == 'nan' or input =='None'):
        input = None
    return input

def get_descriptions_and_helptexts(field_api_name, new_dataframe, old_dataframe):
    new_description = convert_empty_to_none(
        bf.find_value_based_on_column_name_and_other_value(new_dataframe, "QualifiedApiName", field_api_name,
                                                           "Description"))
    new_help_text = convert_empty_to_none(
        bf.find_value_based_on_column_name_and_other_value(new_dataframe, "QualifiedApiName", field_api_name,
                                                           "InlineHelpText"))
    old_description = convert_empty_to_none(
        bf.find_value_based_on_column_name_and_other_value(old_dataframe, "QualifiedApiName", field_api_name,
                                                           "Description"))
    old_help_text = convert_empty_to_none(
        bf.find_value_based_on_column_name_and_other_value(old_dataframe, "QualifiedApiName", field_api_name,
                                                           "InlineHelpText"))
    return new_description, old_description, new_help_text, old_help_text

def field_descriptions_and_helptexts_same(new_description, old_description, new_help_text, old_help_text):
    if (new_description==old_description and new_help_text == old_help_text): #Need to cast the old things to string because otherwise it reads them as a numpy Nan
        return True
    return False

## Connect with salesforce instance
loginInfo = json.load(open(bc.login))
username = loginInfo['username']
password = loginInfo['password']
security_token = loginInfo['security_token']
domain = bc.domain
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id)

mdapi = sf.mdapi

dataframe_dict = bf.convert_files_to_dataframes_dict('write_descriptions')
for dataframe_key in dataframe_dict:

    # read the descriptions of all fields
    dataframe = dataframe_dict[dataframe_key]
    object_api_name = dataframe_key[0:dataframe_key.find("_field")]
    custom_object = mdapi.CustomObject.read(object_api_name)
    print("Updating object: "+object_api_name)

    # See if there are changes
    system_dataframe = bf.perform_field_query(object_api_name,sf)

    #write the changes
    custom_fields = []
    for i, field_api_name in enumerate(dataframe.loc[:, "QualifiedApiName"]):
        new_description, old_description, new_help_text, old_help_text = get_descriptions_and_helptexts(field_api_name,old_dataframe=system_dataframe, new_dataframe=dataframe)

        if not field_descriptions_and_helptexts_same(new_description, old_description, new_help_text, old_help_text):

            if bf.query_yes_no("Are you sure you want to re-write descriptions for object " + object_api_name + " and field " + field_api_name+"? \n"
                "Old description: "+ str(old_description)+" --> new description: "+str(new_description)+"\n"
                  "Old help text: "+ str(old_help_text)+" --> new help text: "+str(new_help_text)+"\n"):

                print("\n") #Cleaner output

                custom_field = mdapi.CustomField(
                    fullName = field_api_name,
                    description = new_description,
                    inlineHelpText = new_help_text
                )
                custom_fields.append(custom_field)

    custom_object.fields = custom_fields
    mdapi.CustomObject.update(custom_object)
    print("Done")