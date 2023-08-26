from typing import List
from typing import Optional
from schemas import Blog, ShowBlog , User , DUser , Show_user , Test, Chat 
from fastapi import FastAPI, Depends, status, Response, HTTPException
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from hashing import Hash , pwd_cxt

import syncDB as s3
import smtp

models.Base.metadata.create_all(engine)

app= FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

guide =(
'''
/sign-up | post | request: 
    user_id: str
    password: str
    email: str
/get-user | get | user_id: str
/delete-user | delete | user_id: str
/set-user-data | post | request:
    user_id: str
    add_method: str [add_msgg]
    msgg: str
/set-user-data-R | post | request:
    user_id: str
    add_method: str [add_response]
    msgg: str
/get-user-data | get:
    user_id: str
/get-user-data-R | get:
    user_id: str
'''
)

@app.get('/')
def home(help=None):
    pass_ = 'admin'
    if help and help==pass_:  return guide
    else: return {'helo! help-> pass help'}

@app.get('/sign-in',status_code=status.HTTP_202_ACCEPTED,tags=['Test'])
def logIN(email: str,password: str):
    response_ = s3.login(user_email=email,password=password)
    if not response_: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with email:{email} not found or password incorrect!')
    return response_

@app.post('/sign-up',status_code=status.HTTP_200_OK,tags=['Test'])
def signUP(request:Test):
    smtp.send_mail(link=f'https://api0w2a.cyclic.cloud/sign-up/verify?name={request.name}&email={request.email}&password={request.password}',name=request.name,email=request.email)
    return f'Check your email at {request.email} for verification link!, as well as SPAM-Folder'

@app.get('/sign-up/verify',status_code=status.HTTP_201_CREATED,tags=['Test-Backennd'])
def verify_(name:str,email:str,password:str):
    print(user_id:= email[:email.rindex("@")])
    response_ = s3.add_user(user_id=user_id,name_=name,email=email,password=password)
    if not response_: raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f'User with id:{user_id} already exists!')
    return {'response':'log-in-verification sucess!'}

@app.get('/get-user',status_code=status.HTTP_200_OK,tags=['Test'])
def get_user(user_id:str):
    return s3.get_user(user_id=user_id)

@app.delete('/delete-user',status_code=status.HTTP_200_OK,tags=['Test'])
def delete_user(user_id:str):
    response_ = s3.del_user(user_id=user_id)
    if not response_: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id:{user_id} not found!') 
    return f'Deleted User with id:{user_id}'

@app.post('/set-user-data',status_code=status.HTTP_200_OK,tags=['Test'])
def user_data(request: Chat):
    return s3.add_user_data(user_id=request.user_id,add_method='add_msgg',msgg=request.msgg)

@app.post('/set-user-data-R',status_code=status.HTTP_200_OK,tags=['Test'])
def user_data(request: Chat):
    return s3.add_user_data(user_id=request.user_id,add_method='add_response',msgg=request.msgg)

@app.get('/get-user-data',status_code=status.HTTP_200_OK,tags=['Test'])
def get_user_data(user_id: str):
    if user_id in (DB := s3.get_DB()).keys():
        return DB[user_id]['message']
    else: return user_id ,"doesn't exist!"

@app.get('/get-user-data-R',status_code=status.HTTP_200_OK,tags=['Test'])
def get_user_data(user_id: str):
    if user_id in (DB := s3.get_DB()).keys():
        return DB[user_id]['response']
    else: return user_id ,"doesn't exist!"

@app.get('/password-reset',status_code=status.HTTP_200_OK,tags=['Test'])
def password_reset(user_email: str,new_password: str):
    return s3.password_reset(user_email=user_email,new_password=new_password)

@app.get('/password-reset/verify',status_code=status.HTTP_202_ACCEPTED,tags=['Test-Backend'])
def password_verify(user_id : str,new_password: str,code: str):
    return s3.password_verify(code=code,new_password=new_password,user_id=user_id)
'''
@app.post('/blog', status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def create(request: Blog , db: Session=Depends(get_db)):
    # new_blog = models.Blog(title=request.title,body=request.body)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    response = s3.put_DB(body=request.model_dump())
    print(request.model_dump())
    return(request.model_dump())

@app.get('/blog', status_code=status.HTTP_200_OK,tags=['Blogs'])
def all(response: Response,db: Session=Depends(get_db), id: int=1):
    # if id==1:
    #     blogs = db.query(models.Blog).all() # gets all blogs
    #     if not blogs: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')  
    # else:
    #     # HTTPException(response_model=ShowBlog)
    #     blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    #     if not blog:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    #         # response.status_code=status.HTTP_404_NOT_FOUND 
    #         # return {'detail': f'blog with id {id} not found'}
    #     blogs = [blog]
    # print(id)
    # return blogs
    response = s3.get_DB()
    print(response)
    return response


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

'''