# Python HTTP API CRUD Demo (with FastAPI)

This project demostrates the use of FastAPI to create a REST API and several CRUD operations. We will be using [FastAPI](https://fastapi.tiangolo.com/). framework to develop the API.

## How to use

1. Create a virtual enviroment and activate it, you can use `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Run on localhost: `uvicorn main:app --reload`

## Authors

Python Endava MED Community 
1. Install dependencies: `pip install fastapi "uvicorn[standard]"`
2. Run on localhost: `uvicorn main:app --reload`

# Graphene
To make use of GraphQL, we'll need to first install Graphene, a Python library that allows us to build GraphQL APIs.

Add it to your requirement.txt file:
graphene==2.1.8

Install:
```
(env)$ pip install -r requirements.txt
```

To use graphql you should go to these paths
```
http://localhost:8000/graphql/saludo
http://localhost:8000/graphql
```

There were implemented two classes which you can execute queries against
To get info form the Saludo class just from http://localhost:8000/graphql/saludo do:
```
query {
  saludo(name: "Michael")
}
```

To get info from CourseType class which is querying a .json file (from http://localhost:8000/graphql) do:
```
{
  getCourse {
    id
    title
    instructor
    publishDate
  }
}
```

To get specific information using course id:
```
{
  getCourse(id: "2") {
    id
    title
    instructor
    publishDate
        }
}
```
It was added a GraphQL mutation to add new courses to our data store or update existing courses.
we can add courses modifying the .json file, passing three parameters with its desired values: id, title and instructor
```
mutation {
  createCourse(
    id: "11" 
    title: "Python Lists" 
    instructor: "Jane Melody"
  ) {
    course {
      id
      title
      instructor
    }
  }
}
``` 
