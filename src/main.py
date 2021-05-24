import jwt
import json
from icecream import ic

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session


from database import SessionLocal, engine
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

JWT_SECRET = 'my_jwt_secret'
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(db:Session=Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = crud.get_user(db, user_id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password")
    
    return schemas.User.from_orm(user)
        

@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    if crud.authenticate_user(db, email=form_data.username, password=form_data.password):
        user = crud.get_user_by_email(db, form_data.username)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password")
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {"access_token" : token, "token_type" : "bearer"}

@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) :
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    return crud.create_user(db=db, user=user)

@app.get('/users/me', response_model=schemas.User)
def get_user(user: schemas.User=Depends(get_current_user)):
    return user




@app.post('/users/tasks', response_model=schemas.Task)
def create_task(task: schemas.Task, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    output_obj = schemas.Task.from_orm(crud.create_user_task(db, task, user.id))
    # ic(output_obj.dict())
    # output_obj["due_dateTime"] = output_obj["due_dateTime"].isoformat()
    # print(output_obj)
    return output_obj
    # return json.dumps({key:val for key, val in output_obj.__dict__.items() if not key.startswith('_')})


@app.get('/users/tasks', response_model=schemas.User)
def show_tasks(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    return crud.get_tasks(db, user.id)
