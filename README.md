# py-jstore

Python Library for using aws dynamodb as a json store.

##Operation:

###put(primary_key=,data=,table=)
    Insert a new item to db if no item exists for primary key
    Or update the attributes for current Item

###get(primary_key=,table=)
    returns Item stored with given primary key
