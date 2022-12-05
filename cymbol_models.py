from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr, HttpUrl

class Image(BaseModel):
    imgs: HttpUrl | None = None

class Product(BaseModel):
    name: str = Field(min_length=6, max_length=255)
    price: float = Field(gt=0.0)
    description: str | None = Field(default=None, max_length=500)
    images: list[Image] | None = Field(default=None, max_items=10)

class Offer(BaseModel):
    products: list[Product] = Field(min_items=1)
    offer_price: float = Field(gt=0.0)
    tags: set[str] | None = Field(default=None, max_length=50, unique_items=True)


class Card(BaseModel):
    card_number: str = Field(min_length=15, max_length=16)
    card_holder_name: str = Field(max_length=255)
    exp_month: int = Field(ge=1, le=31)
    exp_year: int = Field(ge=2000, le=2100)

class Customer(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    age: int | None = Field(default=None, lt=200)
    card: list[Card] | None = None
    joined_on: date | None = None
    profile_picture: Image | None = None

class Account(BaseModel):
    acc_holder: str = Field(max_length=255)
    acc_num: str = Field(min_length=9, max_length=17)
    bank_name: str = Field(max_length=255)
    ifsc_code: str = Field(min_length=11, max_length=11)


class Seller(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    age: int | None = Field(default=None, lt=200)
    account: Account
    joined_on: date | None = None
    products: list[Product] | None = None
    profile_picture: Image | None = None

class Order(BaseModel):
    id: int = Field(ge=0)
    custome: Customer
    seller: Seller
    product: Product
    is_cod: bool = True
    is_cancled: bool = False
    is_delivered: bool = False
    status: str = "Placed"
