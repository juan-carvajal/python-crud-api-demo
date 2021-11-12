# Python
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Graphql
import graphene
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from schemaql import CourseType
import json

# Fastapi
from fastapi import (
    FastAPI, UploadFile, status,
    Query, Path
)


# Models
class Item(BaseModel):
    title: str
    description: str
    # img: Optional[UploadFile] = None

class DBItem(Item):
    db_id: int
    date: datetime

class OutItem(Item):
    data: datetime

# Model grahql
class Queryqlsaludo(graphene.ObjectType):
    saludo = graphene.String(name=graphene.String(default_value=", Unknown!"))
    def resolve_saludo(self, info, name):
        return "Hello " + name
class Queryql(graphene.ObjectType):
  course_list = None
  get_course = graphene.Field(graphene.List(CourseType), id=graphene.String())
  async def resolve_get_course(self, info, id=None):
    with open("./courses.json") as courses:
      course_list = json.load(courses)
    if (id):
      for course in course_list:
        if course['id'] == id: return [course]
    return course_list

class CreateCourse(graphene.Mutation):
  course = graphene.Field(CourseType)

  class Arguments:
    id = graphene.String(required=True)
    title = graphene.String(required=True)
    instructor = graphene.String(required=True)
    publish_date = graphene.String()

  async def mutate(self, info, id, title, instructor):
    with open("./courses.json", "r+") as courses:
      course_list = json.load(courses)

      for course in course_list:
        if course['id'] == id:
          raise Exception('Course with provided id already exists!')

      course_list.append({"id": id, "title": title, "instructor": instructor})
      courses.seek(0)
      json.dump(course_list, courses, indent=2)
    return CreateCourse(course=course_list[-1])
class Mutation(graphene.ObjectType):
  create_course = CreateCourse.Field()
#

app = FastAPI()

# Graphql Path
app.add_route(
    "/graphql/saludo", 
    GraphQLApp(schema=graphene.Schema(query=Queryqlsaludo))
)
app.add_route(
    "/graphql/", 
    GraphQLApp(schema=graphene.Schema(query=Queryql, mutation=Mutation),
    executor_class=AsyncioExecutor)
)




# Root Paht
@app.get(
    path="/",
    tags=['Home',]
)
def api_description():
    """
    # Root path
    Returns the information of version and an important message for the world
    """
    return {
        "message": "Hello World",
        "status": "Amazing Dev Week",
        "Version": "1.0.0"
    }

# CURD 
## get a list of items
@app.get(
    path='/items',
    tags=['items',]
)
async def get_a_list_of_items(
    limit: Optional[int] = Query(10, len=100, ge=1),
    offset: Optional[int] = Query(0, ge=1)
):
    """
    # Get a list of items
    
    Return all the 
    
    ## Parameters
        
    - **Query parameters**:
        - *limit* = (OPTIONAL[int]) It define how many items you want to get, the max value is 100
        - *offset* =  (OPTIONAL[int]) apply an offset from the list of element that you get
    """
    return {
        'limit': limit,
        'offset': offset
    }


## get a single post
@app.get(
    path="/items/{item_id}",
    tags=['items',],
)
def get_an_item(
    item_id: int = Path(..., ge=1),
    complete_data: Optional[bool] = False
):
    """
    # Get a single item from an ID
    
    Search and item from the database bringing the ID
    
    ## Parameters
    
    - **Path parameters**:
        - *item_id* = the ID from the post that you want to search, it is a positive integer number
        
    - **Query parameters**:
        - *complete_data* = (OPTIONAL[booelan]) It define if you want all the information form a post or only the title and description
    """
    
    # TODO: query to data base
    return {
        "item_id": item_id,
        "complete": complete_data
    }

@app.post(
    path='/items',
    status_code=status.HTTP_201_CREATED,
    tags=['items',],
)
async def create_an_item(item: Item):
    """
    # Create a new Item
    
    Bring the basic information from a Item to create it in the data base, this information is:
    - title
    - description
    - image file [optional]
    
    ## Parameters
    
    - **Body parameters**:
        - *title* (string) = the item title
        - *description* (string) = the item description
        - *image file* (optional[file]) = an image that referens the item
    """
    return item

@app.put(
    path='/item/{item_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['items',]
)
async def update_an_item(
    item: Item,
    item_id: int = Path(..., ge=1)
):
    """
    # Update an Item from data base
    
    Bring the ID and the basic information from a Item to update it in the data base
    
    ## Parameters
    
    - **Path parameters**:
        - item_id (int) = the id from the item that you want to delete, is a positive integer value
    
    - **Body parameters**:
        - *title* (string) = the item title
        - *description* (string) = the item description
        - *image file* (optional[file]) = an image that referens the item
    """
    pass

@app.delete(
    path='/item/{item_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['items',]
)
async def delete_an_item(
    item_id: int = Path(..., ge=1),
):
    """
    # Delete an item from data base

    Bring the ID from an item to delete that one

    ## Parameters

    - **Path parameters**:
        - *item_id* (int) = the id from the item that you want to delete, is a positive integer value
    """
    pass

# External API
@app.get(
    path='/get-qr-code',
    tags=['third API',]
)
async def create_a_qr_code():
    pass