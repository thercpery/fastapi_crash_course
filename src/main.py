from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

app = FastAPI()
_services.create_database()


@app.post("/users", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session = Depends(_services.get_db)):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use")

    return _services.create_user(db=db, user=user)


@app.get("/users", response_model=List[_schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: _orm.Session = Depends(_services.get_db)):
    users = _services.get_all_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = Depends(_services.get_db)):
    user = _services.get_user(db=db, user_id=user_id)

    # If no user
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


@app.post("/users/{user_id}/posts", response_model=_schemas.Post)
def create_post(user_id: int, post: _schemas.PostCreate, db: _orm.Session = Depends(_services.get_db)):
    if _services.get_user(db=db, user_id=user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return _services.create_post(db=db, post=post, user_id=user_id)


@app.get("/posts", response_model=List[_schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, db: _orm.Session = Depends(_services.get_db)):
    posts = _services.get_all_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session = Depends(_services.get_db)):
    post = _services.get_post(db=db, post_id=post_id)

    # If no post
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session = Depends(_services.get_db)):
    if _services.get_post(db=db, post_id=post_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or is already deleted.")

    _services.delete_post(db=db, post_id=post_id)

    return {
        "message": "Post successfully deleted."
    }


@app.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(post_id: int, post: _schemas.PostCreate, db: _orm.Session = Depends(_services.get_db)):
    if _services.get_post(db=db, post_id=post_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or is already deleted.")

    return _services.update_post(db=db, post=post, post_id=post_id)
