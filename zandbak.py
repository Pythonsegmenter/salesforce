import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re


a = "Account_field_record_count.csv"
object_api_name = "Account"
field_api_name = "Account_number"
old_help_text = "None"
new_help_text = "useful"
print("Are you sure you want to re-write descriptions for object " + object_api_name + " and field " + field_api_name+"? \n"
    "Old description: "+ old_help_text+" ||| new description: "+new_help_text+"\n"
      "Old help text: "+ old_help_text+" ||| new help text: "+new_help_text+"\n")


# ## Connect with salesforce instance
# loginInfo = json.load(open(bc.login))
# username = loginInfo['username']
# password = loginInfo['password']
# security_token = loginInfo['security_token']
# domain = bc.domain
# session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
# sf = Salesforce(instance=instance, session_id=session_id)

