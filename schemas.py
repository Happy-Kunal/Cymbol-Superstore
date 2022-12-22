from datetime import date

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr, HttpUrl

from pydantic import ValidationError

class ImageBase(BaseModel):
    img: HttpUrl
    desc: str = Field(default="", max_length=255)
    product_id: int = Field(ge=0)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "img": "https://example.com/foo.jpg",
                "desc": "cool image",
                "product_id": 1001
            }
        }

class ImageIn(ImageBase):
    pass

class ImageOut(ImageIn):
    id: int = Field(ge=0)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1001,
                "img": "https://example.com/foo.jpg",
                "desc": "cool image",
                "product_id": 1001
            }
        }



class ProductBase(BaseModel):
    name: str = Field(min_length=6, max_length=255)
    price: float = Field(gt=0.0)
    desc: str = Field(default="", max_length=500)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "some very cool product",
                "price": 100.01,
                "desc": "freshly prepared from very cool ingredients",
                "product_id": 1001
            }
        }

class ProductIn(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int = Field(ge=0)
    imgs: list[ImageOut] = Field(default=[], max_items=10)
    seller_id: int
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
                        "img": "https://example.com/foo.jpg",
                        "desc": "foo",
                    },
                    {
                        "id": 1002,
                        "img": "https://example.com/bar.jpg",
                        "desc": "bar",
                    },
                    {
                        "id": 1003,
                        "img": "https://example.com/baz.jpg",
                        "desc": "baz",
                    }   
                ],

                "seller_id": 1001,
            }
        }

class ProductDB(ProductOut):
    pass




# TODO: implement in future
# class Offer(BaseModel):
#     product_ids: list[int] = Field(min_items=1, ge=0)
#     offer_price: float = Field(gt=0.0)
#     tags: set[str] = Field(default=[], max_length=50)
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "products": [1001, 1002, 1003],
#                 "offer_price": 70.00,
#                 "tags": ["black friday sale"]
#             }
#         }



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


class CardIn(CardBase):
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2000, le=2100)

    class Config:
        schema_extra = {
            "example": {
                "card_number": "1234" "5678" "9101" "1121",
                "card_holder_name": "Foo Bar",
                "exp_month": 11,
                "exp_year": 2024            
            }
        }


class CardOut(CardBase):
    customer_id: int = Field(ge=0)
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "card_number": "1234" "5678" "9101" "1121",
                "card_holder_name": "Foo Bar",
                "customer_id": 1001,
            }
        }


class CardDB(CardOut):
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2000, le=2100)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "card_number": "1234" "5678" "9101" "1121",
                "card_holder_name": "Foo Bar",
                "customer_id": 1001,
                "exp_month": 11,
                "exp_year": 2024            
            }
        }



class UserBase(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr
    age: int | None = Field(default=None, ge=10, le=200)
    joined_on: date | None = None
    # TODO: add profile picture in future
    # profile_picture: Image | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "age": 20,
                "joined_on": "2003-04-12", 
            }
        }


class CustomerIn(UserBase):
    pass


class CustomeOut(UserBase):
    id: int = Field(ge=0)
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "age": 20,
                "joined_on": "2003-04-12", 
            }
        }


class CustomerDB(CustomeOut):
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
                "hashed_password": "<HashedPassword>"
            }
        }



class AccountBase(BaseModel):
    acc_number: str = Field(min_length=9, max_length=17)
    acc_holder: str = Field(max_length=255)
    bank_name: str = Field(max_length=255)
    ifsc_code: str | None = Field(default=None, min_length=11, max_length=11)
    
    class Config:
        schema_extra = {
            "example": {
                "acc_number": "1234" "5678" "9101" "1121",
                "acc_holder": "Foo Bar",
                "bank_name": "Baz Bank",
                "ifsc_code": "bazb0123456"
            }
        }


class AccountIn(AccountBase):
    pass


class AccountOut(AccountBase):
    seller_id: int
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "acc_number": "1234" "5678" "9101" "1121",
                "acc_holder": "Foo Bar",
                "bank_name": "Baz Bank",
                "ifsc_code": "bazb0123456",
                "seller_id": 1001,
            }
        }


class AccountDB(AccountOut):
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "acc_number": "1234" "5678" "9101" "1121",
                "acc_holder": "Foo Bar",
                "bank_name": "Baz Bank",
                "ifsc_code": "bazb0123456",
                "seller_id": 1001,
            }
        }



class OrderBase(BaseModel):
    price: float = Field(ge=0)
    is_cod: bool = True
    is_cancled: bool = False
    is_delivered: bool = False
    status: str  | None = "Placed"

    customer_id: int = Field(ge=0)
    seller_id: int = Field(ge=0)
    product_id: int = Field(ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "price": 100.00,
                "is_cod": True,
                "is_cancled": False,
                "is_delivered": True,
                "status": "payment received",
                
                "customer_id": 1002,
                "seller_id": 1003,
                "product_id": 1001,
            }
        }

class OrderIn(OrderBase):
    pass

class OrderOut(OrderIn):
    id: int = Field(ge=0)
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1001,
                "price": 100.00,
                "is_cod": True,
                "is_cancled": False,
                "is_delivered": True,
                "status": "payment received",
                
                "customer_id": 1002,
                "seller_id": 1003,
                "product_id": 1001,
            }
        }

class OrderDB(OrderOut):
    pass




class SellerIn(UserBase):
    pass


class SellerOut(SellerIn):
    id: int = Field(ge=0)
    products: list[ProductOut] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "joined_on": "2003-04-12",
                "products": []
            }
        }


class SellerDB(UserBase):
    hashed_password: str
    products: list[ProductDB] = []
    accounts: list[AccountDB] = []
    orders: list[OrderDB] = []
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1002,
                "name": "Foo Bar",
                "email": "foo.bar@example.com",
                "joined_on": "2003-04-12",
                "accounts": [
                    {
                        "acc_number": "1234" "5678" "9101" "1121",
                        "acc_holder": "Foo Bar",
                        "bank_name": "Baz Bank",
                        "ifsc_code": "bazb0123456"
                    },
                ],
                "products": [],
                "hashed_password": "<HashedPassword>"
            }
        }



class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id: int
    username: str = Field(alias="sub")
    isSeller: bool = Field(default=False, alias="seller")



if __name__ == "__main__":
    pass