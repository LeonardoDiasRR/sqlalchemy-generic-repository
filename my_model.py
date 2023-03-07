from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from declarative_base import Base


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    employees = relationship("Employee", backref="employees", lazy="subquery")

    def __repr__(self):
        return f'Department(id={self.id}, name={self.name})'


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    # department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return f'Employee(id={self.id}, name={self.name}, email={self.email}, department_id={self.department_id})'