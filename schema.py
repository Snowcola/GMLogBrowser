# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee

class SearchResult(graphene.Union):
    class Meta:
        types = (Department, Employee)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    search = graphene.List(SearchResult, q=graphene.String())
    employee = graphene.Field(Employee, name=graphene.String())

    def resolve_employee(self, info, **args):
        name = args.get("name")
        print(name)
        employee_query = Employee.get_query(info)
        employees = employee_query.filter(EmployeeModel.name.like(name)).first()
        return employees
    # Allows sorting over multiple columns, by default over the primary key
    def resolve_search(self, info, **args):
        q = args.get("q")
        department_query = Department.get_query(info)
        employee_query = Employee.get_query(info)
        
        departments = department_query.filter((DepartmentModel.name.contains(q))).all()
        employees = employee_query.filter((EmployeeModel.name.contains(q))).all()

        return departments + employees 



    all_employees = SQLAlchemyConnectionField(EmployeeConnections)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)

schema = graphene.Schema(query=Query, types=[Department, Employee, SearchResult])