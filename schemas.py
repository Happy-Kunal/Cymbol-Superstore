from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr, HttpUrl

from pydantic import ValidationError

class Image(BaseModel):
    id: int
    desc: str = Field(default="", max_length=255)
    img: HttpUrl | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1001,
                "desc": "cool image",
                "img": "https://example.com/foo.jpg"
            }
        }

class Product(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=6, max_length=255)
    price: float = Field(gt=0.0)
    desc: str = Field(default="", max_length=500)
    imgs: list[Image] = Field(default=[], max_items=10)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1001,
                "name": "some very cool product",
                "price": 100.01,
                "desc": "freshly prepared from very cool ingredients",
                "imgs": [
                    {
                        "id": 1001,
                        "desc": "foo",
                        "img": "https://example.com/foo.jpg"
                    },
                    {
                        "id": 1002,
                        "desc": "bar",
                        "img": "https://example.com/bar.jpg"
                    },
                    {
                        "id": 1003,
                        "desc": "baz",
                        "img": "https://example.com/baz.jpg"
                    }   
                ]
            }
        }


class Offer(BaseModel):
    product_ids: list[int] = Field(min_items=1, ge=0)
    offer_price: float = Field(gt=0.0)
    tags: set[str] = Field(default=[], max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "products": [1001, 1002, 1003],
                "offer_price": 70.00,
                "tags": ["black friday sale"]
            }
        }



class CardBase(BaseModel):
    card_number: str = Field(min_length=15, max_length=16)
    card_holder_name: str = Field(max_length=255)

    class Config:
        schema_extra = {
            "example": {
                "card_number": "1234" "5678" "9101" "1121",
                "card_holder_name": "Foo Bar",
            }
        }

class CardOut(CardBase):
    class Config:
        schema_extra = {
            "example": {
                "card_number": "1234" "5678" "9101" "1121",
                "card_holder_name": "Foo Bar",
            }
        }

class CardDB(CardBase):
    card_number: str = Field(min_length=15, max_length=16)
    card_holder_name: str = Field(max_length=255)
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2000, le=2100)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "card_number": "1234" "5678" "9101" "1121",
                "card_holder_name": "Foo Bar",
                "exp_month": 11,
                "exp_year": 2024            
            }
        }


class UserBase(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(max_length=255)
    email: EmailStr
    age: int | None = Field(default=None, lt=200)
    joined_on: date | None = None
    profile_picture: Image | None = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "joined_on": None,
                "profile_picture": None  
            }
        }

class CustomeOut(UserBase):
    class Config:
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "joined_on": None,
                "profile_picture": None  
            }
        }

class CustomerDB(UserBase):
    cards: list[CardDB] | None = None
    hashed_password: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "cards": [
                    {
                        "card_number": "1234" "5678" "9101" "1121",
                        "card_holder_name": "Foo Bar",
                        "exp_month": 11,
                        "exp_year": 2024
                    }
                ],
                "joined_on": None,
                "profile_picture": None,
                "hashed_password": "HashedPassword"
            }
        }


class Account(BaseModel):
    acc_holder: str = Field(max_length=255)
    acc_num: str = Field(min_length=9, max_length=17)
    bank_name: str = Field(max_length=255)
    ifsc_code: str = Field(min_length=11, max_length=11)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "acc_holder": "Foo Bar",
                "acc_num": "1234" "5678" "9101" "1121",
                "bank_name": "Baz Bank",
                "ifsc_code": "bazb0123456"
            }
        }

class SellerOut(UserBase):
    product_ids: list[int] = []

    class Config:
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "joined_on": None,
                "profile_picture": None,
                "product_ids": [1001, 1002, 1003]
            }
        }

class SellerDB(UserBase):
    account: Account
    product_ids: list[int] = []
    hashed_password: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "joined_on": None,
                "profile_picture": None,
                "account": {
                    "acc_holder": "Foo Bar",
                    "acc_num": "1234" "5678" "9101" "1121",
                    "bank_name": "Baz Bank",
                    "ifsc_code": "bazb0123456"
                },
                "product_ids": [1001, 1002, 1003],
                "hashed_password": "HashedPassword"
            }
        }

class Order(BaseModel):
    id: int = Field(ge=0)
    customer_id: int = Field(ge=0)
    seller_id: int = Field(ge=0)
    product_ids: list[int] = Field(ge=0)
    price: float = Field(ge=0)
    is_cod: bool = True
    is_cancled: bool = False
    is_delivered: bool = False
    status: str = "Placed"
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1001,
                "customer_id": 1002,
                "seller_id": 1003,
                "product_ids": [1001, 1002, 1003],
                "price": 100.00,
                "is_cod": True,
                "is_cancled": False,
                "is_delivered": True,
                "status": "payment received"
            }
        }




if __name__ == "__main__":
    try:
        customer1 = CustomerDB(
            id = 1001,
            name="Foo Bar",
            email="foo.bar@example.com",
        )

        print(customer1)
        print()


        customer2 = CustomerDB(
            id = 1002,
            name="Foo Bar",
            email="foo.bar@example.com",
            cards=[
                CardDB(
                    card_number="1234" "5678" "9101" "1121",
                    card_holder_name="Foo Bar",
                    exp_month=11,
                    exp_year=2024
                )
            ]
        )

        print(customer2)
        print()

        customer3 = CustomerDB(
            id = 1003,
            name="Foo Bar",
            email="veryLongEmail" + "foo" * 100 + "@example.com" # must fail
        )

        print(customer3)
        print()

    except ValidationError as e:
        print(e)