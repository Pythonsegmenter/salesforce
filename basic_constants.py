
#Things to retrieve
relate_by_selection = True #Determines if we relate objects by selecting specific objects or by ignoring specific objects

selection_list = ['Block Price', 'Contracted Price', 'Custom Price Book', 'Discount Schedule', 'Discount Tier', 'Price Action', 'Price Book', 'Price Book Entry', 'Price Condition', 'Price Rule']
selection_list_api_names = ['Approval','Opportunity','SBQQ__Quote__c','SBQQ__QuoteLine__c','Order','OrderItem','Product2','Pricebook2','PricebookEntry','Contract','Asset','SBQQ__Subscription__c'] #A selection list using api names

ignore_list = ['Activity', 'Social Persona'] #Search for relations in between all objects except for the ones in this list (activity & social persona are empty dataframes and cause errors)
api_ignore_list = ['Quote','QuoteLineItem'] #For objects that have duplicate labels.

object_properties = "Label,QualifiedApiName,Description" # ,DeploymentStatus --> no spaces here ,Description -->description only available in api tooling box

#Things to print
print_links = True
print_fields = False

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
## Sales cloud + CPQ
# 'Approval', 'Account','Opportunity','Quote','Quote Line','Order','Order Product','Product','Price Book','Price Book Entry','Contract','Asset','Subscription'
# 'Approval','Opportunity','SBQQ__Quote__c','SBQQ__QuoteLine__c','Order','OrderItem','Product2','Pricebook2','PricebookEntry','Contract','Asset','SBQQ__Subscription__c'
## Product data management
# ['Additional Document', 'Attribute Item', 'Attribute Set', 'Configuration Attribute', 'Configuration Rule', 'Error Condition', 'Product', 'Product Action', 'Product Attribute Set', 'Product Feature', 'Product Option', 'Product Rule', 'Upgrade Source']
