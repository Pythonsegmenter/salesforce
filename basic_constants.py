
#Things to retrieve
relate_by_selection = True #Determines if we relate objects by selecting specific objects or by ignoring specific objects

selection_list = ['Account','Contact','User','Task','Event','Account / BU', 'Address'] #Search for relations in between the objects in this list
selection_list_api_names = ['MTLS_Address__c'] #A selection list using api names

ignore_list = ['Activity', 'Social Persona'] #Search for relations in between all objects except for the ones in this list (activity & social persona are empty dataframes and cause errors)
api_ignore_list = ['Quote'] #For objects that have duplicate labels.

object_properties = "Label,QualifiedApiName,Description" # ,DeploymentStatus --> no spaces here ,Description -->description only available in api tooling box

#Things to print
print_links = False
print_fields = True

#Domain to login to
login = "login_uat.json" #login_dev.json or login_uat.json
domain = 'test' #login or test

#check_field_usage_script
print_records = False

#Old selection lists:
## High level
#'Account','Contact','Opportunity','Quote','Order','Price Book','Contract','Asset','Subscription','Product','Order Product','Case','Invoice','Entitlement'
## Foundations
# 'Account','Contact','User','Task','Event','Account / BU', 'Address'
