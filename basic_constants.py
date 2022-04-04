relate_by_selection = False #Determines if we relate objects by selecting specific objects or by ignoring specific objects

selection_list = ['Account', 'Contact', 'Account / BU'] #Search for relations in between the objects in this list
ignore_list = [] #Search for relations in between all objects except for the ones in this list

#For testing
stop_limit = 99999 #Used for testing. Put on 99999 if no limit is desired.