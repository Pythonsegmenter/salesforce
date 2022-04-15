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
custom_object = mdapi.CustomObject.read("Account")
custom_field = mdapi.CustomField(
    fullName = "AccountNumber",
    description = "Not used",
    inlineHelpText = "Not used"
)
custom_object.fields = [custom_field]

mdapi.CustomObject.update(custom_object)
print("Done")