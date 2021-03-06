import graphene
from graphene import relay
from graphene.types.json import JSONString
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class CreateEmployee(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        hobbies = JSONString()
        results = JSONString()
        department_id = graphene.Int()

    ok = graphene.Boolean()
    employee = graphene.Field(Employee)

    @classmethod
    def mutate(cls, _, info, **args):
        employee = EmployeeModel(name=args.get('name'),
                                 hobbies=args.get('hobbies'),
                                 results=args.get('results'),
                                 department_id=args.get('department_id'))
        db_session.add(employee)
        db_session.commit()
        ok = True
        return CreateEmployee(employee=employee, ok=ok)


class UpdateEmployee(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        hobbies = JSONString()
        results = JSONString()
        department_id = graphene.Int()

    ok = graphene.Boolean()
    employee = graphene.Field(Employee)

    @classmethod
    def mutate(cls, _, info, **args):
        query = Employee.get_query(info)

        employee = query.filter(EmployeeModel.name == args.get('name')).first()
        employee.department_id = args.get('department_id')
        employee.hobbies = args.get('hobbies')
        employee.results = args.get('results')
        db_session.commit()
        ok = True

        return UpdateEmployee(employee=employee, ok=ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    employees = SQLAlchemyConnectionField(Employee)
    departments = SQLAlchemyConnectionField(Department)
    employee = graphene.Field(Employee, name=graphene.String())

    def resolve_employee(self, info, name):
        query = Employee.get_query(info)
        return query.filter(EmployeeModel.name == name).first()


class MyMutations(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Department, Employee])
