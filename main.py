# Python
import io
import tempfile
from typing import Optional
from pydantic import (
    BaseModel, HttpUrl
)
from datetime import datetime

# Graphql
import graphene
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from schemaql import CourseType
import json

# Fastapi
from fastapi import (
    FastAPI, status,
    Query, Path, Body
)
from fastapi.responses import FileResponse
# third party
import requests
import qrcode
from PIL import Image

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


## get a single item
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

## Create a new item
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

## update information
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


## Delete an item
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

def get_cat_img():
    # request to Cat API
    req = requests.get('https://thatcopy.pw/catapi/rest')
    # get the URl from img
    cat_url = req.json()['url']
    img_req = requests.get(cat_url)
    # create a temparary imga file
    cat_img = tempfile.TemporaryFile()
    cat_img.write(img_req.content)
    return cat_img

def create_qr_img( content: str, qr_size: int = 2):
    img = Image.open(get_cat_img())
    img = img.resize((round(img.size[0]*0.1), round(img.size[1]*0.1)))

    qr = qrcode.QRCode(box_size=qr_size)
    qr.add_data(content)
    qr.make()
    
    img_qr = qr.make_image()
    
    pos = (img.size[0] - img_qr.size[0], img.size[1] - img_qr.size[1])
    img.paste(img_qr, pos)

    return img

@app.post(
    path='/qr-cat',
    tags=['third API',]
)
async def create_a_qr_code(
    url: HttpUrl = Body(..., example="https://www.dacacode.com"),
    qr_size: Optional[int] = Query(2, ge=1, le=5)
):
    qr_code = create_qr_img(url, qr_size)
    qr_code.save('img.png')
    
    # temp = tempfile.TemporaryFile()
    # temp.write(qr_code.tobytes())
    
    return FileResponse(
        'img.png',
        media_type='image/png',
        filename='qr-code.png'
    )