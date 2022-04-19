import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re


a = "Account_field_record_count.csv"
print(a.find("_field"))
print(a[0:7])

# ## Connect with salesforce instance
# loginInfo = json.load(open(bc.login))
# username = loginInfo['username']
# password = loginInfo['password']
# security_token = loginInfo['security_token']
# domain = bc.domain
# session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
# sf = Salesforce(instance=instance, session_id=session_id)

