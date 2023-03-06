from connection import Session
from sqlalchemy import and_, or_
from sqlalchemy.orm import Query


class GenericPagination:

    # A Pagination object represents a single page of query results.

    def __init__(self, query, page, page_size):

        if not isinstance(query, Query):
            raise TypeError(f'"query" is not an instance of sqlalchemy.orm.Query.')

        if not isinstance(page, int):
            raise TypeError(f'"page" must be integer.')

        if page < 1:
            raise Exception(f'"page" must be greater then or equal 1')

        if not isinstance(page, int):
            raise TypeError(f'"page_size" must be integer.')

        if page_size < 1:
            raise Exception(f'"page_size" must be greater then or equal 1')

        # the SQLAlchemy Query object being paginated (sqlalchemy.orm.query.Query):.
        self.query = query

        # the current page number (int).
        self.page = page

        # the number of results per page (int).
        self.page_size = page_size

        # the total number of results in the query (int).
        self.total = self.query.count()

        # the total number of pages (int)
        if self.total % self.page_size == 0:
            self.pages = int(self.total / self.page_size)
        else:
            self.pages = int(self.total / self.page_size) + 1

        # the page number of the previous page, or None if this is the first page.
        if self.page - 1 >= 1:
            self.prev_num = self.page - 1
        else:
            self.prev_num = None

        # the page number of the next page, or None if this is the last page.
        if self.page + 1 <= self.pages:
            self.next_num = self.page + 1
        else:
            self.next_num = None

        offset = (self.page - 1) * self.page_size
        limit = self.page_size

        self.items = query.offset(offset).limit(limit).all()

        if self.page > self.pages:
            raise Exception(f'Page number "{self.page}" can not be greater then total of pages "{self.pages}". '
                            f'Check the page size informed.')

    # return a Pagination object for the previous page, or None if this is the first page.
    # def prev(self):
    #     pass

    # return a Pagination object for the next page, or None if this is the last page.
    # def next(self):
    #     pass

    # generate a sequence of page numbers to display in a pagination widget.
    def page_numbers(self):
        return list(range(1, self.pages+1))


def model_to_dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


class GenericRepository:

    def __init__(self, Model):
        self.model = Model

        self.config = {
            'MAX_PAGE_SIZE': 100,
            'AUTO_COMMIT': True
        }

        # Get the model's columns name
        self.columns = [column.name for column in Model.__table__.columns]

        # Get the model's primary keys names
        self.primary_keys = [primary_key.name for primary_key in Model.__table__.primary_key.columns.values()]

        # Get model's not nullable columns name
        self.not_nullable_columns = [x.name for x in Model.__table__.columns if not x.nullable and x.name not in
                                     self.primary_keys]
        # self.not_nullable_columns = list(set(self.not_nullable_columns) - set(self.primary_keys))

        # # check if a column is nullable
        # print(User.__table__.c.name.nullable)  # False
        # print(User.__table__.c.age.nullable)  # True

    def verify_columns(self, **kwargs):
        # Check if all kwargs key exist in model columns
        for key in kwargs.keys():
            if key not in self.columns:
                raise Exception(f'Field "{key}" does not exist in model "{self.model.__table__}".')

        return True

    def verify_primary_keys(self, **kwargs):
        # Check if all model´s primary keys are present in kwargs
        pks = [x for x in kwargs if x in self.primary_keys]
        pks_missing = list(set(self.primary_keys) - set(pks))
        if len(pks_missing) > 0:
            raise Exception(f'Primary key {pks_missing} missing.')

    def verify_not_nullable_columns(self, **kwargs):
        # Verify if all not nullable columns are present in kwargs
        fields_missing = list(set(self.not_nullable_columns) - set(kwargs.keys()))
        if len(fields_missing) > 0:
            raise Exception(f'Not null field missing {fields_missing}')

        # Check if all not nullable columns is None or empty
        for column in self.not_nullable_columns:
            if kwargs[column] is None:
                raise Exception(f'Not nullable column "{column}" is None.')
            elif kwargs[column] is False and not isinstance(kwargs[column], bool):
                raise Exception(f'Not nullable column "{column}" is empty.')

        return True

    # Function to verify if Model PKs are present in **kwargs
    def get_primary_keys(self, **kwargs):
        # Get PKs names from **kwargs
        pks = {}
        for key, value in kwargs.items():
            if key in self.primary_keys:
                pks[key] = value

        # Check if all Model PKs are present in **kwargs
        diff_primary_keys = list(set(self.primary_keys) - set(pks.keys()))
        if len(diff_primary_keys) > 0:
            raise Exception(f'Mising Primary Keys {diff_primary_keys}')

        return pks

    def create(self, **kwargs):
        # Check columns informed in kwargs
        if self.verify_columns(**kwargs):
            # Check if not nullable columns are present and are not empty
            self.verify_not_nullable_columns(**kwargs)

        with Session() as session:
            try:
                my_model = self.model(**kwargs)
                session.add(my_model)
                session.commit()
                return model_to_dict(my_model)
            except Exception as e:
                session.rollback()
                raise e

    def create_all(self, list_items):
        if not isinstance(list_items, list):
            raise TypeError(f'{list_items} must be a list.')

        for item in list_items:
            if not isinstance(item, dict):
                raise TypeError(f'{item} must be a dictionary')

            # Check columns informed in kwargs
            if self.verify_columns(**item):
                # Check if not nullable columns are present and are not empty
                self.verify_not_nullable_columns(**item)

        with Session() as session:
            try:
                # insert the rows
                session.bulk_insert_mappings(self.model, list_items)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                raise e

    # Function that read ONE item in the database based on its PKs
    # kwargs are model PK key,values pairs
    # keys must be a valid Model PKs columns
    def read(self, **kwargs):
        # Exctract PKs names from **kwargs
        pks = self.get_primary_keys(**kwargs)

        # Create a filter condition based on the specified search criteria
        filter_condition = None
        for column_name, column_value in pks.items():
            if column_value is not None:
                column_filter = getattr(self.model, column_name) == column_value
                filter_condition = column_filter if filter_condition is None else filter_condition & column_filter

        with Session() as session:
            # Execute the search and return the results
            result = session.query(self.model).filter(filter_condition).first()

            return result

    def update(self, **kwargs):
        # Check columns informed in kwargs
        self.verify_columns(**kwargs)

        # Check if primary keys were informed
        self.verify_primary_keys(**kwargs)

        my_model = self.read(**kwargs)
        if my_model:
            for key in kwargs:
                if key:
                    setattr(my_model, key, kwargs[key])

        with Session() as session:
            try:
                session.add(my_model)
                session.commit()
                return model_to_dict(my_model)
            except Exception as e:
                session.rollback()
                raise e

    def update_many(self, search_params, **kwargs):
        # Check if keys in **kwargs are Model valid columns
        self.verify_columns(**kwargs)

        # Create OR and AND filters from search parameters
        or_filters, and_filters = self._create_filter_expression(search_params)
        # If any (OR_FILTERS or AND_FILTERS) are True, return True
        filter_expression = any([or_filters, and_filters])

        if not filter_expression:
            raise Exception('No filter expression informed.')
        else:
            with Session() as session:
                query = session.query(self.model)
                # Add filters to query
                if and_filters:
                    query = query.filter(and_(*and_filters))
                if or_filters:
                    query = query.filter(or_(*or_filters))

                try:
                    updated = query.filter(filter_expression).update(kwargs)
                    session.commit()
                    return updated

                except Exception as e:
                    session.rollback()
                    raise Exception(e)

    def delete(self, **kwargs):
        # Check if keys in **kwargs are Model valid columns
        self.verify_columns(**kwargs)

        deleted = None
        with Session() as session:
            try:
                my_model = self.read(**kwargs)
                if my_model:
                    deleted = session.delete(my_model)
                    session.commit()

            except Exception as e:
                session.rollback()
                raise e

        return deleted

    def delete_many(self, search_params):

        # Create OR and AND filters from search parameters
        or_filters, and_filters = self._create_filter_expression(search_params)
        # If any (OR_FILTERS or AND_FILTERS) are True, return True
        filter_expression = any([or_filters, and_filters])

        if not filter_expression:
            raise Exception('No filter expression informed.')
        else:
            with Session() as session:
                query = session.query(self.model)
                # Add filters to query
                if and_filters:
                    query = query.filter(and_(*and_filters))
                if or_filters:
                    query = query.filter(or_(*or_filters))

                try:
                    deleted = query.filter(filter_expression).delete()
                    session.commit()
                    return deleted
                except Exception as e:
                    session.rollback()
                    raise Exception(e)

    def search(self, page=1, page_size=10, sort=None, search_params=None):
        # search_params is a list of dictionary with field, operator, value and conjuction
        # See the follow example
        # search_params = [
        #     {"field": "name", "operator": "like", "value": "John", "conjunction": "and"},
        #     {"field": "age", "operator": ">=", "value": 25, "conjunction": "or"},
        #     {"field": "email", "operator": "ilike", "value": "%example.com", "conjunction": "and"},
        # ]

        if page_size > self.config["MAX_PAGE_SIZE"]:
            page_size = self.config["MAX_PAGE_SIZE"]

        # Get the sort columns and directions from 'sort' parameter
        sort_columns = []
        if sort:
            order_values = sort.split(',')
            for sort in order_values:
                if sort[0] in ['-', '+']:
                    if sort[0] == '-':
                        sort_direction = 'desc'
                    else:
                        sort_direction = 'asc'

                    if sort[1:] in self.columns:
                        sort_columns.append((sort[1:], sort_direction))
                    else:
                        pass
                        # Ignore if sort column is not in model columns

        # If no sort columns were informed, use PKs ASC as sort columns and direction
        # defaults values for sort column and direction
        if len(sort_columns) <= 0:
            for pk in self.primary_keys:
                sort_columns.append((pk, 'asc'))

        # Construct the order_by clause dynamically
        order_by = []
        for column, sort in sort_columns:
            column_obj = getattr(self.model, column)
            if sort == "asc":
                order_by.append(column_obj.asc())
            elif sort == "desc":
                order_by.append(column_obj.desc())

        # Create OR and AND filters from search parameters
        or_filters, and_filters = self._create_filter_expression(search_params)
        # If any (OR_FILTERS or AND_FILTERS) are True, return True
        filter_expression = any([or_filters, and_filters])

        with Session() as session:
            query = session.query(self.model)
            # query = session.query(self.model).join(self.model.related_objects)

            # Add filters to query
            if and_filters:
                query = query.filter(and_(*and_filters))
            if or_filters:
                query = query.filter(or_(*or_filters))

            if filter_expression:
                # Search for filter expression created
                query.filter(filter_expression).order_by(*order_by)
            else:
                # If no filter were informed, search all items
                query.order_by(*order_by)

            # Do Pagination
            # Wrap the query with Query class to use paginate method (thanks chatGPT!)
            # paginated_query = Query(query)
            # paginated_results = paginated_query.paginate(page=page, per_page=page_size)

            paginated_results = GenericPagination(query, page=page, page_size=page_size)

            return paginated_results

    # Construct the filter from search_params and returns '_or' and '_and' objects
    def _create_filter_expression(self, search_params=None):

        # Define a dictionary that maps operator symbols to SQLAlchemy operators
        operators = {
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
            "like": lambda x, y: x.like(y),
            "ilike": lambda x, y: x.ilike(y),
            "in": lambda x, y: x.in_(y),
            "not in": lambda x, y: x.notin_(y),
        }

        conjunctions = ['and', 'or']

        filter_expression = None
        and_filters = []
        or_filters = []
        # Validate search parameters
        # Check if search_params is a list
        if search_params is not None:
            if not isinstance(search_params, list):
                raise TypeError(f'"search_params" is not a list.')

            for param in search_params:
                if not isinstance(param, dict):
                    raise TypeError(f'Param "{param}" is not a dict.')

                # Check if all params informed have a correspondent model column
                if param["field"] not in self.columns:
                    raise Exception(f'Field "{param["field"]}" does not exist in model "{self.model.__table__}".')

                # Check if the operator is valid
                if param["operator"] not in operators:
                    raise Exception(f'Operator "{param["operator"]}" invalid')

                if param["conjunction"] not in conjunctions:
                    raise Exception(f'Conjuction "{param["conjunction"]}" invalid.')

                # Dynamically construct the filter expression using the search parameters
                for param in search_params:
                    operator_func = operators.get(param["operator"])
                    if operator_func:
                        filter_expression = operator_func(getattr(self.model, param["field"]), param["value"])
                        if param["conjunction"].lower() == 'or':
                            or_filters.append(filter_expression)
                        else:
                            and_filters.append(filter_expression)

        return or_filters, and_filters
