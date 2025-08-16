import datetime
import random
import string
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from . import models, schemas
from .database import get_db
from .settings import jwt_settings
import smtplib
from email.mime.text import MIMEText

router = APIRouter()

def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
    return encoded_jwt

@router.post("/request-otp")
def request_otp(email_schema: schemas.EmailSchema, db: Session = Depends(get_db)):
    email = email_schema.email
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    otp_code = ''.join(random.choices(string.digits, k=6))
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    otp = models.OTP(email=email, otp_code=otp_code, expires_at=expires_at)
    db.add(otp)
    db.commit()

    print(f"OTP for {email}: {otp_code}")

    try:
        msg = MIMEText(f"Your OTP is: {otp_code}")
        msg['Subject'] = "Your OTP Code"
        msg['From'] = "noreply@example.com"
        msg['To'] = email
        with smtplib.SMTP('localhost', 1025) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

    return {"message": "OTP sent to your email."}

@router.post("/verify-otp", response_model=schemas.Token)
def verify_otp(otp_schema: schemas.OTPSchema, db: Session = Depends(get_db)):
    email = otp_schema.email
    otp_code = otp_schema.otp

    otp = db.query(models.OTP).filter(
        models.OTP.email == email,
        models.OTP.otp_code == otp_code
    ).first()

    if not otp or otp.expires_at < datetime.datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    db.delete(otp)
    db.commit()

    access_token_expires = datetime.timedelta(minutes=jwt_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
