## uvicorn app.main:app --reload --no-server-header

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='apidb',user='postgres',password='!!C0mpaq2532', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error) 
        time.sleep(2)
   
my_posts = [{"title": "title of post 1", "content": "content post 1", "id": 1},  {"title": "title of post 2", "content": "content post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
        for i, p in enumerate(my_posts):
            if p['id'] == id:
                return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO post (title, content,published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    #post_dict = post.dict()
    #post_dict['id'] = randrange(10, 1000000)
    #my_posts.append(post_dict)
    return {"data": new_post}

@app.get("/posts/latest") ## Check order of path parameters for routes where {id} could match
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}") ## ID of the the record - "Path Parameter"
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):

    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (str(id),)))
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    return {"data": post}