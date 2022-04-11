
#Things to retrieve
relate_by_selection = True #Determines if we relate objects by selecting specific objects or by ignoring specific objects

selection_list = ['Task','Event'] #Search for relations in between the objects in this list
ignore_list = ['Activity', 'Social Persona'] #Search for relations in between all objects except for the ones in this list (activity & social persona are empty dataframes and cause errors)

object_properties = "Label,QualifiedApiName,Description" # ,DeploymentStatus --> no spaces here ,Description -->description only available in api tooling box

#Things to print
print_links = False
print_fields = True

#Domain to login to
login = "login_dev.json" #login_dev.json or login_uat.json
domain = 'login' #login or test

#For testing
stop_limit = 99999 #Used for testing. Put on 99999 if no limit is desired.

