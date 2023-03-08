# sqlalchemy-generic-repository module
It's a generic repository module to handle any sqlalchemy model, providing basic CRUD methods and a flexible search method.
The module contains two main classes: GenericRepository and GenericPagination. GenericRepository provides the methods to handle the sqlalchemy model with CRUD methods and a flexible search method. GenericPagination class is used paginate the search. It is returned by GenericRepository.search() method.

## GenericRepository methods:
### create(**kwargs)
Create one item in corresponding table in database. You can pass key/values to method, where keys must correspond to model fields. The method returns a model instance of corresponding row inserted into database table. Not nullable fields defined in model are mandatory. **Do not pass primary keys fields to create() method, unless you are absolutly sure you what you are doing.**

Example:
```
repo_epmloyee = GenericRepository(EmployeeModel)
repo_epmloyee.create(name="John", email="john@email.com")
```

### create_all(list_items)
Create all items in list. Each item in the list is a dictionary with key/values. Return True if success or None. Keys must corresponding to model fields. Not nullable fields in model are mandatory.

Example:
```
employees_list = [
 {"name": "John", "email": "john@email.com"},
 {"name": "Peter", "email": "peter@email.com"}
]
epmloyee = GenericRepository(EmployeeModel)
employee.create_all(employees_list)
```

### read(**kwargs)
Read one item based on it's primary key(s). Return a instance of model retreived or None if no row where found.
```
epmloyee = GenericRepository(EmployeeModel)
employee.read(id=1)
```


### update(**kwargs)
Update one item in database based on it's primary key(s). Return a model instance of updated item.
```
epmloyee = GenericRepository(EmployeeModel)
employee.update(id=1, name="John Peter", email="jpeter@email.com")
```


### update_many(search_params, **kwargs)
Update many items based on informed searh parameters. Return number of rows affected.
```
employees_search_params = [
{"field": "name", "operator": "like", "value": "%John%", "conjunction": "and"}
]
epmloyee = GenericRepository(EmployeeModel)
employee.update_many(search_params=employees_search_params, email="john.peter@email.com")
```

In the example above, all employees with name "John" in the name will have email updated to "john.peter@email.com" in database.


### delete(**kwargs)
Delete one item in database based on it's primary key(s). Return number of rows affeced.
```
epmloyee = GenericRepository(EmployeeModel)
employee.delete(id=1)
```
It will delete the employee with ID=1


### delete_many(search_params)
Delete many items based on informed searh parameters. Return number of rows affeced.
```
employees_search_params = [
{"field": "name", "operator": "like", "value": "%John%", "conjunction": "and"}
]
epmloyee = GenericRepository(EmployeeModel)
employee.delete_many(search_params=employees_search_params)
```
In the example above, all employees with name "John" in the name will be deleted from database.

In the example above, all employees with name "John" in the name will have email updated to "john.peter@email.com".

### search(page=1, page_size=10, sort=None, search_params=None)
A flexible search method.
You must inform page number and page size for the search. The max page size can configured in config["MAX_PAGE_SIZE"] attribute of GenericRepository class (default is 100).

Sort order is optionsl. If not informed, it will sort the search for the model primary key(s) ascending. To determine sort order, pass the paramenter 'sort=' with a string containing plus signal (ascending) or minus signal (descending), joined with the name of the field you want to sort. Example, if you want to sort a search for name in ascending order, inform the parameter: sort="+name". To sort for multiple fields, just separete each one with a comma. Example: sort="+name,-email"

The 'search_params' is a list of dictionaries containing the search criterias. Example:
search_params = [

     {"field": "name", "operator": "like", "value": "%John%", "conjunction": "and"},     
     {"field": "age", "operator": ">=", "value": 25, "conjunction": "or"},     
     {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"}
]

 The operators supported are: ["==", "!=", ">", "<", ">=", "<=", "like", "ilike", "in", "not in", "is", "is not"]
 The conjunctions supported are: ["and", "or"]

# What the GenericRepository does not do (yet):
Complex search with joins or grouping clouses. Although, you can declare a lazy loading parameter in your models relationships that retreival simple joins. See: https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html

