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
    # department.update(id=2, name='SRH/SR/PF/RR')

    # DELETE
    # department.delete(id=25)

    employee.create(name='Leonardo', department_id=1)
    employee.create(name='Ramos', department_id=1)
    employee.create(name='Ricardo', department_id=1)
    employee.create(name='Ross', department_id=1)
    employee.create(name='Ronald', department_id=2)
    employee.create(name='Glaudeci', department_id=2)
    employee.create(name='Edgard', department_id=2)


    # SEARCH Departments an it's Employees (no filter)
    print('\nDepartments with employees:')
    for dept in department.search():
        print(dept)
        if dept.employees:
            for emp in dept.employees:
                print(emp)
