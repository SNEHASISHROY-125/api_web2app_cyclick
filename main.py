from typing import List
from typing import Optional
from schemas import Blog, ShowBlog , User , DUser , Show_user
from fastapi import FastAPI, Depends, status, Response, HTTPException
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from hashing import Hash , pwd_cxt

models.Base.metadata.create_all(engine)

app= FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def create(request: Blog , db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[ShowBlog],tags=['Blogs'])
def all(response: Response,db: Session=Depends(get_db), id: int=1):
    if id==1:
        blogs = db.query(models.Blog).all() # gets all blogs
        if not blogs: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')  
    else:
        # HTTPException(response_model=ShowBlog)
        blog = db.query(models.Blog).filter(models.Blog.id==id).first()
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
            # response.status_code=status.HTTP_404_NOT_FOUND 
            # return {'detail': f'blog with id {id} not found'}
        blogs = [blog]
    print(id)
    return blogs

@app.delete('/blog', status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def destroy(id: int, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

@app.put('/blog', status_code=status.HTTP_202_ACCEPTED,tags=['Blogs'])
def update(id: int, request: Blog, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return 'updated'


@app.get('/user', status_code=status.HTTP_200_OK, response_model=List[Show_user],tags=['Users'])
def get_user(id:Optional[int]=0,db: Session=Depends(get_db)):
    if id==0:
        users = db.query(models.Users).all()
    else:
        user = db.query(models.Users).filter(models.Users.id==id).first()
        users = [user]
    return users

@app.post('/user', status_code=status.HTTP_201_CREATED,tags=['Users'])
def create_user(request: User, db: Session=Depends(get_db)):
    # hashed_pwd = pwd_cxt.hash(request.password)
    new_user = models.Users(name=request.name,email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    # return {'data': 'user created'}

@app.delete('/user', status_code=status.HTTP_200_OK,tags=['Users'])
def delete_user(request: DUser , db: Session=Depends(get_db) ):
    user = db.query(models.Users).filter(models.Users.name==request.name)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with Name {request.name} not found')
    if not pwd_cxt.verify(request.password, user.first().password):
        print(Hash.bcrypt(request.password))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'password incorrect')
    user.delete(synchronize_session=False)
    db.commit()
    return f'User with Name:{request.name} was deleted'
