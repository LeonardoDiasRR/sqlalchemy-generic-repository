# sqlalchemy-generic-repository module
It's a generic repository module of classes to handle any sqlalchemy model, providing basic CRUD function and a flexible search function.
The module contains two classes: GenericRepository and GenericPagination

## GenericRepository methods:
### create(self, **kwargs)
Create one item in corresponding table in database. You can pass key/values to function, where keys must correspond to model fields. The method returns an model instance of corresponding to the row inserted into database table. Not nullable fields defined in model are mandatory.
Example:
epmloyee = GenericRepository()
employee.create(name="John", email="john@email.com")
returns: {"id": 1, "name": "John", "email": "john@email.com")

### create_all(self, list_items)
Create all items in list. Each item in the list is a dictionary with key/values. Return True if success or None. Keys must corresponding to model fields. Not nullable fields in model are mandatory.
Example:
employees_list = [
 {"name": "John", "email": "john@email.com"},
 {"name": "Peter", "email": "peter@email.com"}
]
epmloyee = GenericRepository()
employee.create_all(employees_list)
Return True if sucess.

### read(self, **kwargs)
Read one item based on it's primary key(s). Return a instance of model retreived or None if no row where found.

### update(self, **kwargs)
Update one item in database based on it's primary key(s). Return a model instance of updated item.

### update_many(self, search_params, **kwargs)
Update many items based on informed searh parameters. Return number of rows affected.

### delete(self, **kwargs)
Delete one item in database based on it's primary key(s). Return number of rows affeced.

### delete_many(self, search_params)
Delete many items based on informed searh parameters. Return number of rows affeced.

### search(self, page=1, page_size=10, sort=None, search_params=None)
A flexible search function.
You must inform page number and page size for the search. The max page size can configured in config["MAX_PAGE_SIZE"] attribute of GenericRepository class (default is 100).

Sort order is optionsl. If not informed, it will sort the search for the model primary key(s) ascending. To determine sort order, pass the paramenter 'sort=' with a string containing plus signal (ascending) or minus signal (descending), joined with the name of the field you want to sort. Example, if you want to sort a search for name in ascending order, inform the parameter: sort="+name". To sort for multiple fields, just separete each one with a comma. Example: sort="+name,-email"

The 'search_params' is a list of dictionaries containing the search criterias. Example:
search_params = [

     {"field": "name", "operator": "like", "value": "%John%", "conjunction": "and"},     
     {"field": "age", "operator": ">=", "value": 25, "conjunction": "or"},     
     {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"}
]

 The operators supported are: ["==", "!=", ">", "<", ">=", "<=", "like", "ilike", "in", "not in"]
 The conjunctions supported are: ["and", "or"]

# What the GenericRepository does not do (yet):
Complex search with joins or grouping clouses.
Perhaps, depending on how are the relationship in your models, GenericSearch can retreival basic joins.

