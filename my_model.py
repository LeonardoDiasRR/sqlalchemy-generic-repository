from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from declarative_base import Base


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    employees = relationship("Employee", back_populates='department', lazy="subquery")

    def __repr__(self):
        return f'Department(id={self.id}, name={self.name})'


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)

    department = relationship("Department", back_populates="employees", lazy="joined")

    def __repr__(self):
        return f'Employee(id={self.id}, name={self.name}, email={self.email}, department_id={self.department_id})'


# Example of many to many relationship
# define association table to establish many-to-many relationship between Book and Author tables
association_table = Table('association', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)


# define Book table
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = relationship('Author', secondary=association_table, back_populates='books', lazy='joined')

    def __repr__(self):
        return f'Book(id={self.id}, title={self.title})'


# define Author table
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship('Book', secondary=association_table, back_populates='authors', lazy='joined')

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'