from pydantic import BaseModel

class EmailSchema(BaseModel):
    email: str

class OTPSchema(BaseModel):
    email: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
