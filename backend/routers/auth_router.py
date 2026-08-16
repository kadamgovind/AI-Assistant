from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import hash_password

router = APIRouter()

@router.post("/signup")
def signup(user: dict, db: Session = Depends(get_db)):
    try:
        email = user.get("email")
        password = user.get("password")

        if not email or not password:
            raise HTTPException(status_code=400, detail="Missing fields")

        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(password)

        new_user = models.User(
            email=email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    except Exception as e:
        print("Signup Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")