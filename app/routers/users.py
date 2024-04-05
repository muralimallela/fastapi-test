from fastapi import APIRouter,status,HTTPException,Depends
from .. import schemas,models,utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate,db : Session = Depends(get_db)):
    
    check_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="An accout is alredy exits with the email provided")
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db : Session = Depends (get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"NO user found with id {id}")
    return user