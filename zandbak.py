# Import pandas library
import basic_functions as bf

a = "account/BU"
print(a.find("/"))

print(a[0:7]+" per "+a[8:])
print(a.find("z"))









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

