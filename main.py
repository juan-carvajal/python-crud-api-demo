# Python
from typing import Optional
from pydantic import (
    BaseModel, HttpUrl
)
from datetime import datetime
# Fastapi
from fastapi import (
    FastAPI, status,
    Query, Path, Body
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


app = FastAPI()


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
    limit: Optional[int] = Query(10, le=100, ge=1),
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
@app.get(
    path='/get-qr-code',
    tags=['third API',]
)
async def create_a_qr_code(
    url: HttpUrl = Body(...)
):
    return {
        "url": url
    }