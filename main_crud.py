# Python
import tempfile
from typing import Optional
from pydantic import (
    BaseModel, HttpUrl
)
from datetime import datetime

from database import get_cats, get_cat, create_cat, update_cat, delete_cat

from fastapi import (
    FastAPI, status,
    Query, Path, Body
)
from fastapi.responses import FileResponse

# Models


class Cat(BaseModel):
    id: Optional[int]
    name: str
    keeper: str
    breed: str


app = FastAPI()

# Root Paht


@app.get(
    path="/",
    tags=['Home', ]
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
# get a list of items

@app.get(
    path='/cats',
    tags=['cats', ]
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
    return get_cats(offset, limit)


# get a single item
@app.get(
    path="/cats/{cat_id}",
    tags=['cats', ],
)
async def get_an_item(
    cat_id: int = Path(..., ge=1),
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

    return get_cat(cat_id)

# Create a new item


@app.post(
    path='/cats',
    status_code=status.HTTP_201_CREATED,
    tags=['cats', ],
)
async def create_an_item(cat: Cat):
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
    return create_cat(cat)

# update information


@app.put(
    path='/cat/{cat_id}',
    tags=['cats', ]
)
async def update_an_item(
    cat: Cat,
    cat_id: int = Path(..., ge=1)
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
    return update_cat(cat, cat_id)


# Delete an item
@app.delete(
    path='/cat/{cat_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['cats', ]
)
async def delete_an_item(
    cat_id: int = Path(..., ge=1),
):
    """
    # Delete an item from data base

    Bring the ID from an item to delete that one

    ## Parameters

    - **Path parameters**:
        - *item_id* (int) = the id from the item that you want to delete, is a positive integer value
    """
    return delete_cat(cat_id)
