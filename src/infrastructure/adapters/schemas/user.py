from pydantic import BaseModel, Field

class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: str
    name: str
