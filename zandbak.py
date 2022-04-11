import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import basic_functions as bf
import basic_constants as bc
import re
a=re.match(".*,?User,.*","(User,Calendar,Group")
b=re.match("User","User")
if re.match(".*,?User,.*","(Pizza,Calendar,Group"):
    print("yes")
else:
    print("no")



# ## Connect with salesforce instance
# loginInfo = json.load(open(bc.login))
# username = loginInfo['username']
# password = loginInfo['password']
# security_token = loginInfo['security_token']
# domain = bc.domain
# session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
# sf = Salesforce(instance=instance, session_id=session_id)
#
# # obj_info = pd.DataFrame(sf.query(
# #         "SELECT name FROM Account")['records'])
# # obj_info = pd.DataFrame(sf.query(
# #         "SELECT Label, Description FROM EntityDefinition WHERE IsCustomizable=True")[
# #                                               'records'])
#
# obj_info = pd.DataFrame(sf.toolingexecute("query/?q=SELECT+Label,Description+from+EntityDefinition+Where+IsCustomizable=True")['records'])
# print("a")










# def check_link(data_type, target_obj_label):
#     """Returns link, link type, match with target object"""
#     if len(data_type)<6: #No look up or master detail
#         return False, False, False
#     elif data_type[0:7]=="Lookup(":
#         if data_type[7:-1]==target_obj_label:
#             return True, "Lookup", True
#         return True, "Lookup", False
#     elif data_type[0:14]=="Master-Detail(":
#         if data_type[14:-1]==target_obj_label:
#             return True, "Master-Detail", True
#         return True, "Master-Detail", False
#
# print(check_link("Lookup(pizza pesto)","pizza pesto"))
# print(check_link("Lookup(pizza pesto)","pizza piano"))
# print(check_link("Master-Detail(pizza pesto)","pizza pesto"))
# print(check_link("Master-Detail(pizza pesto)","pizza piano"))
# print(check_link("text","pizza piano"))

