from pydantic import BaseModel, ConfigDict, Field


class FarmerRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6, max_length=100)
    language: str = "en"


class FarmerLogin(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6, max_length=100)


class FarmerResponse(BaseModel):
    id: int
    name: str
    phone: str
    language: str

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"