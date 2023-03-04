from generic_repository import GenericRepository
from my_model import Department, Employee
from declarative_base import Base
from connection import engine

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':

    department = GenericRepository(Department)
    employee = GenericRepository(Employee)

    # CREATE
    # For create a table item, just call function 'create' informing a pair of field_name=value of fields you want
    # to populate. DO NOT PASS PRIMARY KEYS TO CREATE FUNCTION! Let SqlAlchemy handle it.
    # Do it only if you know what you are doing.
    # department.create(name='SETEC')
    # department.create(name='SELOG')

    # UPDATE
    # department.update(id=6, department_id=1)

    # DELETE
    # department.delete(id=25)

    employee_list = [
        {"name": 'Nilvania', "department_id": 2},
        {"name": "Livia", "department_id": 2},
        {"name": "Liz", "department_id": 2},
        {"name": "Lucas", "department_id": 2},
        {"name": "Olaf", "department_id": 2},
        {"name": "Chanel", "department_id": 2}
    ]


    # EMPLOYEES

    # employee.create_all(employee_list)

    update_employee_list = [
        {"id": 1, "department_id": 2},
        {"id": 4, "department_id": 1}
    ]

    # employee.update(id=6, department_id=1)
    employee.update_all(update_employee_list)

    # employee.create(name='Leonardo', department_id=1)
    # employee.create(name='Ramos', department_id=1)
    # employee.create(name='Ricardo', department_id=1)
    # employee.create(name='Ross', department_id=1)
    # employee.create(name='Ronald', department_id=2)
    # employee.create(name='Glaudeci', department_id=2)
    # employee.create(name='Edgard', department_id=2)


    # DELETE MANY
    search_params = [
        {"field": "department_id", "operator": "==", "value": "2", "conjunction": "and"}
    ]

    # employee.delete_many(search_params)

    employee_search_params = [
        {"field": "department_id", "operator": "==", "value": "1", "conjunction": "and"}
        # {"field": "age", "operator": ">=", "value": 25, "conjunction": "or"},
        # {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"},
    ]

    # SEARCH Departments an it's Employees (no filter)
    # print('\nDepartments with employees:')
    # for dept in department.search():
    #     print(dept)
    #     if dept.employees:
    #         for emp in dept.employees:
    #             print('\t', emp)

    pagination = employee.search(page=3, page_size=4)

    print('\nEmployees:')
    for idx, emp in enumerate(pagination.items, start=1):
        print(idx, emp)

    print('\nPagination:')
    print('Total items:', pagination.total)
    print('Page size:', pagination.page_size)
    print('Total pages:', pagination.pages)
    print('Current page:', pagination.page)
    print('Page number list:', pagination.page_numbers())



