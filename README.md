# sqlalchemy-generic-repository package
It's a generic repository package of classes to handle any sqlalchemy model, providing basic CRUD function and a flexible search function.

## GenericRepositort methods:
### create(self, **kwargs)
Create one item in corresponding table in database

### create_all(self, list_items)
Create all items in list. Each item in the list is a dictionary with model key, values. Example:
employee_list = [
 {"name": "John", "email": "john@email.com"},
 {"name": "Peter", "email": "peter@email.com"}
]

### read(self, **kwargs)
Read one item based on it's primary key(s)

### update(self, **kwargs)
Update one item in database based on it's primary key(s)

### update_all(self, list_items: list)
Update many items based on informed searh parameters 

### delete(self, **kwargs)
Delete one item in database based on it's primary key(s)

### delete_many(self, search_params)
Delete many items based on informed searh parameters

### search(self, page=1, page_size=10, sort=None, search_params=None)
A flexible search function.
You must inform page number and page size for the search. The page size can be at maximum of value configured in self.config["MAX_PAGE_SIZE"] attribute (default is 100).
Sort order is optionsl. If not informed, it will sort the search for the model primary key(s) ascending. To determine sort order, pass the paramenter 'sort' with a string containing plus (ascending) or minus (descending) signal, joined with the name of the field you want to sort. Example, if you want to sort a search for name in ascending order, infor the parameter: sort="+name". To sort for multiple fields, just separete each one with a comma. Example: sort="+name,-email"

The 'search_params' is a list of dictionaries containing the search criterias. Example:
search_params = [
     {"field": "name", "operator": "like", "value": "John", "conjunction": "and"},
     {"field": "age", "operator": ">=", "value": 25, "conjunction": "or"},
     {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"}
 ]
 The operators supported are: ["==", "!=", ">", "<", ">=", "<=", "like", "ilike", "in", "not in"]
 The conjunctions supported are: ["and", "or"]

