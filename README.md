### Flask GraphQl example ###

Flask + Graphene + SqlAlchemy

Resources:

- http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
- https://github.com/graphql-python/graphene-sqlalchemy
- https://github.com/graphql-python/graphene

Access url after install: http://localhost:5001/graphql

Examples:

Get specific employee:
```
query {
  employee(name:"Peter") {
    id,
    name
  }
}
```

Get employee list:
```
query {
  employees {
    edges {
      node {
        name
        hiredOn
        departmentId
        department {
          name
        }
      }
    }
  }
}
```

Create new employee:

```
mutation {
  createEmployee(name:"Andrei", departmentId:1) {
    employee {
      id,
      name
      departmentId
    }
    ok
  }
}

mutation {
  createEmployee(name:"Andrei", hobbies:"\"['asdad', 'ddddd']\"", departmentId:1) {
    employee {
      id,
      name
      departmentId
    }
    ok
  }
}
```

Update employee department_id:

```
mutation {
  updateEmployee(name: "Peter", departmentId:2) {
    employee {
      name,
      departmentId
    }
  }
}
```
