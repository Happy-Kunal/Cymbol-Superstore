from pydantic import EmailStr, HttpUrl
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, get_db
import crud
import models, schemas, security, extras

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    security.router,
    prefix="/auth",
    tags=["auth"],
)



#####################################################################
#                           get methods                             #
#####################################################################

@app.get("/get/customers/{id}", response_model=schemas.CustomeOut)
async def get_customer(id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db=db, customer_id=id)
    if customer:
        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/customers/email/{email}", response_model=schemas.CustomeOut)
async def get_customer_by_email(email: EmailStr, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_email(db=db, email=email)
    if customer:
        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/image/{image_id}", response_model=schemas.Image)
async def get_image_by_id(image_id: int, db: Session = Depends(get_db)):
    image = crud.get_image(db=db, image_id=image_id)
    if image:
        return image
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/orders/{id}", response_model=schemas.OrderOut)
async def get_order(id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db=db, order_id=id)
    if order:
        return order
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/products", response_model=schemas.MultipleProducts)
async def get_products(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(offset=offset).limit(limit=limit).all()
    if products:
        return {"products": products}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/products/{id}", response_model=schemas.ProductOut)
async def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db=db, product_id=id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/sellers/{id}", response_model=schemas.SellerOut)
async def get_seller(id: int, db: Session = Depends(get_db)):
    seller = crud.get_seller(db=db, seller_id=id)
    if seller:
        return seller
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/get/sellers/email/{email}", response_model=schemas.SellerOut)
async def get_seller_by_email(email: EmailStr, db: Session = Depends(get_db)):
    seller = crud.get_seller_by_email(db=db, email=email)
    if seller:
        return seller
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )

@app.get("/get/me/cards", response_model=schemas.MultipleCards)
async def get_my_cards(db: Session = Depends(get_db), user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)):
    if (not user.isSeller):
        cards = crud.get_cards(db, customer_id=user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Customers are allowed to have bank cards\n"
                    "Instead try fetching your Bank Account details"
        )

    if cards:
        return {"cards": cards}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )

@app.get("/get/me/accounts", response_model=schemas.MultipleAccounts)
async def get_my_bank_accounts(db: Session = Depends(get_db), user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)):
    if (user.isSeller):
        accounts = crud.get_cards(db, customer_id=user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Sellers are allowed to have bank accounts\n"
                    "Instead try fetching your Cards details"
        )

    if accounts:
        return {"accounts": accounts}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


#####################################################################
#                           post methods                            #
#####################################################################

# TODO after Reading about OAuth and JWT tokens

#####################################################################
#                           put methods                             #
#####################################################################

# TODO after reading about OAuth and JWT tokens

#####################################################################
#                           delete methods                          #
#####################################################################

# TODO after reading about OAuth and JWT tokens
