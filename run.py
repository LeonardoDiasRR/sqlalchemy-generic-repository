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
    # print(department.create(name='SELOG'))

    departments_list = [
        {"name": "SETEC"},
        {"name": "Casa"}
    ]

    # department.create_all(departments_list)

    # UPDATE
    # dep = department.update(id=2, name='Minha Casa')
    # print(f'{dep} atualizado')
    # for emp in dep.employees:
    #     print(f'\t{emp}')

    # DELETE
    # department.delete(id=25)

    # SEARCH DEPARTMENT
    # dep = department.search()
    # for d in dep.items:
    #     print(d)
    #     for emp in d.employees:
    #         print(f'\t{emp}')

    # EMPLOYEES
    new_employees_list = [
        # {"name": "Andre Ramos", "department_id": 1},
        # {"name": "Andre Ross", "department_id": 1},
        # {"name": "Raí", "department_id": 1},
        # {"name": "Ricardo", "department_id": 1},
        # {"name": "Rubinaldo", "department_id": 1},
        # {"name": "Luiz Otávio", "department_id": 1},
        # {"name": "Leonardo", "department_id": 2},
        # {"name": "Nilvania", "department_id": 2},
        # {"name": "Livia", "department_id": 2},
        # {"name": "Liz", "department_id": 2},
        # {"name": "Lucas", "department_id": 2},
        {"name": "Olaf", "email": "olaf@emil.com", "department_id": 1},
        {"name": "Chanel", "email": "chanel@email.com", "department_id": 1}
    ]

    # print(employee.create_all(new_employees_list), 'Created')

    # CREATE SINGLE EMPLOYEE
    # print(employee.create(name="Ibrahim", department_id="1"))
    # employee.create(name="Uilian", department_id="1")
    # employee.create(name="Willian", department_id="1")
    # employee.create(name="Alice", department_id="1")

    update_employee_list = [
        {"id": 1, "department_id": 2},
        {"id": 4, "department_id": 1}
    ]

    # UPDATE
    # print(employee.update(id=16, name="Alice", department_id=1))
    # employee.update_all(update_employee_list)

    # emp = employee.create(name='Alice Maiara', department_id=1)
    # print(f'Created: {emp}')

    # employee.create(name='Ramos', department_id=1)
    # employee.create(name='Ricardo', department_id=1)
    # employee.create(name='Ross', department_id=1)
    # employee.create(name='Ronald', department_id=2)
    # employee.create(name='Glaudeci', department_id=2)
    # employee.create(name='Edgard', department_id=2)

    employee_update_search_params = [
        {"field": "name", "operator": "ilike", "value": "%alice%", "conjunction": "and"}
        # {"field": "age", "operator": ">=", "value": 25, "conjunction": "or"},
        # {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"},
    ]

    # updated = employee.update_many(search_params=employee_update_search_params, name="Alice Maiara")
    # print(f'{updated} Rows affected')

    # DELETE ONE ROW
    # deleted = employee.delete(id=2)
    # print(f'{deleted} rows deleted.')

    # DELETE MANY ROWS
    delete_params = [
        {"field": "name", "operator": "==", "value": "Alice Maiara", "conjunction": "and"}
        # {"field": "id", "operator": "in", "value": [14, 15], "conjunction": "and"}
    ]

    # deleted = employee.delete_many(delete_params)
    # print(f'{deleted} rows deleted.')

    employee_search_params = [
        {"field": "name", "operator": "ilike", "value": "%olaf%", "conjunction": "and"},
        {"field": "email", "operator": "is", "value": None, "conjunction": "and"}
        # {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"},
    ]

    # SEARCH Departments an it's Employees (no filter)
    # print('\nDepartments with employees:')
    # for dept in department.search():
    #     print(dept)
    #     if dept.employees:
    #         for emp in dept.employees:
    #             print('\t', emp)

    # emp = employee.read(id=1)
    # print(emp)
    # print(emp.department.name)

    pagination = employee.search(page=1, page_size=50, search_params=employee_search_params)

    print('\nEmployees:')
    for idx, emp in enumerate(pagination.items, start=1):
        print(idx, emp)

    print('\nPagination:')
    print('Total items:', pagination.total)
    print('Page size:', pagination.page_size)
    print('Total pages:', pagination.pages)
    print('Current page:', pagination.page)
    print('Next page num:', pagination.next_num)
    print('Prev page num:', pagination.prev_num)
    print('Page number list:', pagination.page_numbers())



